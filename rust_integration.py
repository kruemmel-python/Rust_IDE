# rust_integration.py
import os
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from cargo_toml_manager import TomlManager
import subprocess


class RustIntegration:
    def __init__(self, parent):
        self.parent = parent
        self.project_path = None
        self.current_file = None  # Hier wird die aktuelle Datei gespeichert
        self.build_mode = 'debug'  # Standard-Modus: debug
        self.gdb_process = None  # Für den Debugger
        self.build_process = QProcess()  # Asynchroner Prozess für den Build
        self.toml_manager = None  # Für die Verwaltung von Cargo.toml

        # Signale für den Build-Prozess
        self.build_process.setProcessChannelMode(QProcess.MergedChannels)
        self.build_process.readyRead.connect(self.read_build_output)
        self.build_process.finished.connect(self.build_finished)

    def get_latest_version(self, crate_name):
        """Verwende 'cargo search', um die neueste Version eines Crates von crates.io zu erhalten."""
        try:
            result = subprocess.run(["cargo", "search", crate_name], capture_output=True, text=True)
            output = result.stdout

            for line in output.splitlines():
                if line.startswith(crate_name):
                    version = line.split('"')[1]  # Extrahiere die Version
                    return version
        except Exception as e:
            print(f"Fehler beim Abrufen der Version für {crate_name}: {e}")
        return None

    def new_project(self):
        """Erstelle ein neues Rust-Projekt im angegebenen Verzeichnis."""
        dir_path = QFileDialog.getExistingDirectory(self.parent, 'Wähle Projektordner')

        if dir_path:
            self.project_path = dir_path
            try:
                # Initialisiere ein neues Rust-Projekt mit cargo
                result = os.system(f'cargo init "{self.project_path}"')
                if result == 0:
                    QMessageBox.information(self.parent, "Erfolg", "Neues Rust-Projekt erstellt!")
                
                    # Initialisiere den TomlManager, um mit Cargo.toml zu arbeiten
                    cargo_toml_path = os.path.join(self.project_path, "Cargo.toml")
                
                    if os.path.exists(cargo_toml_path):
                        # Lade und passe die Cargo.toml Datei automatisch an
                        self.toml_manager = TomlManager(self.project_path, self.parent.output_area)
                        cargo_data = self.toml_manager.load_cargo_toml()
                    
                        # Optional: Standard-Abhängigkeiten oder Profile hinzufügen
                        cargo_data['profile'] = {
                            'dev': {
                                'debug': True
                            }
                        }
                    
                        # Speichere die aktualisierte Cargo.toml
                        self.toml_manager.save_cargo_toml(cargo_data)
                        self.parent.output_area.append("Cargo.toml Datei erfolgreich initialisiert.")
                    else:
                        QMessageBox.critical(self.parent, "Fehler", "Cargo.toml Datei wurde nicht gefunden.")
                else:
                    QMessageBox.critical(self.parent, "Fehler", "Projekt konnte nicht erstellt werden.")
            except Exception as e:
                QMessageBox.critical(self.parent, "Fehler", f"Fehler beim Erstellen des Projekts: {e}")


    def open_main_rs(self):
        main_rs_path = os.path.join(self.project_path, 'src', 'main.rs')
        if os.path.exists(main_rs_path):
            try:
                with open(main_rs_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    self.parent.editor.setPlainText(code)
                    self.current_file = main_rs_path  # Aktuell geöffnete Datei setzen
            except UnicodeDecodeError:
                with open(main_rs_path, 'r', encoding='latin-1') as f:
                    code = f.read()
                    self.parent.editor.setPlainText(code)
                    self.current_file = main_rs_path


    def open_cargo_toml(self):
        """Öffne die Cargo.toml Datei im Editor."""
        cargo_toml_path = os.path.join(self.project_path, 'Cargo.toml')
        if os.path.exists(cargo_toml_path):
            try:
                with open(cargo_toml_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    self.parent.editor.setPlainText(code)
                    self.current_file = cargo_toml_path  # Setze den Pfad der aktuell geöffneten Datei
                    self.parent.output_area.append(f"Cargo.toml Datei geöffnet: {cargo_toml_path}")
            except Exception as e:
                self.parent.output_area.append(f"Fehler beim Öffnen der Cargo.toml Datei: {e}")
        else:
            QMessageBox.warning(self.parent, "Warnung", "Cargo.toml Datei nicht gefunden.")



    def save_project(self):
        """Speichert die aktuell geöffnete Datei und fügt fehlende Bibliotheken zur Cargo.toml hinzu."""
        if self.current_file:
            try:
                # Speichere die aktuell geöffnete Datei
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    code = self.parent.editor.toPlainText()
                    f.write(code)
                self.parent.output_area.append(f"Datei erfolgreich gespeichert: {self.current_file}")

                # Falls es sich nicht um die Cargo.toml handelt, prüfen wir auf Bibliotheken
                if not self.current_file.endswith("Cargo.toml"):
                    # Analysiere den Code nach Bibliotheken
                    self.add_dependencies_from_code()

            except Exception as e:
                self.parent.output_area.append(f"Fehler beim Speichern der Datei: {e}")
        else:
            QMessageBox.warning(self.parent, "Warnung", "Keine Datei zum Speichern geöffnet.")




    def add_dependencies_from_code(self):
        """Analysiere den Code und füge fehlende Abhängigkeiten der Cargo.toml hinzu."""
        try:
            code = self.parent.editor.toPlainText()
            self.parent.output_area.append("Analysierter Code:\n" + code)

            # Extrahiere alle Bibliotheken, die mit 'use' verwendet werden
            used_libraries = self.extract_libraries_from_code(code)

            # Lade die aktuelle Cargo.toml-Datei
            if self.toml_manager:
                cargo_data = self.toml_manager.load_cargo_toml()

                # Überprüfe, ob die Bibliotheken bereits in der Cargo.toml existieren
                for library in used_libraries:
                    if 'dependencies' not in cargo_data:
                        cargo_data['dependencies'] = {}

                    if library not in cargo_data['dependencies']:
                        # Suche nach der neuesten Version der Bibliothek
                        version = self.get_latest_version(library)
                        if version:
                            self.parent.output_area.append(f"Füge {library} (Version: {version}) zur Cargo.toml hinzu...")
                            cargo_data['dependencies'][library] = version
                        else:
                            self.parent.output_area.append(f"Konnte keine Version für {library} finden. Bibliothek wird nicht hinzugefügt.")
            
                # Speichere die aktualisierte Cargo.toml
                self.toml_manager.save_cargo_toml(cargo_data)
                self.parent.output_area.append("Cargo.toml wurde erfolgreich aktualisiert.")

        except Exception as e:
            self.parent.output_area.append(f"Fehler beim Hinzufügen von Abhängigkeiten zur Cargo.toml: {e}")


    def extract_libraries_from_code(self, code):
        """
        Extrahiere Bibliotheksnamen aus dem Rust-Code basierend auf 'use'-Statements.
        """
        libraries = set()
        lines = code.splitlines()

        for line in lines:
            line = line.strip()
            if line.startswith('use'):
                # Extrahiere den Teil nach 'use', entferne unnötige Zeichen wie Semikolon
                lib = line.split(' ')[1].split('::')[0].replace(';', '').strip()
                libraries.add(lib)

        return libraries


    def set_debug_mode(self):
        self.build_mode = 'debug'
        QMessageBox.information(self.parent, "Build-Modus", "Modus auf Debug gesetzt.")

    def set_release_mode(self):
        self.build_mode = 'release'
        QMessageBox.information(self.parent, "Build-Modus", "Modus auf Release gesetzt.")

    def run_rust_code(self):
        """Führt das Rust-Projekt aus (cargo run)."""
        try:
            if self.project_path:
                # Nur .rs-Dateien oder Cargo.toml speichern
                if self.current_file.endswith('.rs') or self.current_file.endswith('Cargo.toml'):
                    self.save_project()
            
                # Führe den Cargo-Befehl aus
                cargo_command = ["cargo", "run"] if self.build_mode == 'debug' else ["cargo", "run", "--release"]
                self.build_process.setWorkingDirectory(self.project_path)
                self.build_process.start(cargo_command[0], cargo_command[1:])
                self.parent.output_area.clear()  # Leere die Ausgabeanzeige
            else:
                QMessageBox.warning(self.parent, "Warnung", "Kein Projekt geöffnet oder erstellt.")
        except Exception as e:
            QMessageBox.critical(self.parent, "Fehler", f"Fehler beim Ausführen des Projekts: {e}")



    def read_build_output(self):
        """Liest die Echtzeit-Ausgabe des Build-Prozesses."""
        output = self.build_process.readAllStandardOutput().data().decode()
        self.parent.output_area.append(output)

    def build_finished(self, exit_code, exit_status):
        """Reagiere, wenn der Build-Prozess beendet ist."""
        if hasattr(self.parent, 'output_area') and self.parent.output_area is not None:
            if exit_status == QProcess.NormalExit and exit_code == 0:
                self.parent.output_area.append("Build erfolgreich abgeschlossen.")
            else:
                self.parent.output_area.append(f"Build fehlgeschlagen. Exit Code: {exit_code}")
        else:
            print(f"Build-Prozess beendet, aber output_area ist nicht verfügbar. Exit Code: {exit_code}")


    def start_debugger(self):
        """Startet den gdb Debugger."""
        if self.project_path:
            self.save_project()
            cargo_build_command = ["cargo", "build"]
            build_process = QProcess(self.parent)
            build_process.setWorkingDirectory(self.project_path)
            build_process.start(cargo_build_command[0], cargo_build_command[1:])
            build_process.waitForFinished()

            executable_path = os.path.join(self.project_path, 'target', 'debug', os.path.basename(self.project_path))
            self.gdb_process = QProcess(self.parent)
            self.gdb_process.setProcessChannelMode(QProcess.MergedChannels)
            self.gdb_process.readyRead.connect(self.read_gdb_output)
            self.gdb_process.start("gdb", [executable_path])

            QMessageBox.information(self.parent, "Debugger", "gdb Debugger gestartet.")
        else:
            QMessageBox.warning(self.parent, "Warnung", "Kein Projekt geöffnet oder erstellt.")

    def read_gdb_output(self):
        """Kontinuierliches Lesen der gdb-Ausgabe."""
        if self.gdb_process and self.gdb_process.canReadLine():
            output = self.gdb_process.readAllStandardOutput().data().decode()
            self.parent.output_area.append(output)

    def send_gdb_command(self, command):
        """Sendet einen Befehl an den gdb-Debugger."""
        if self.gdb_process:
            self.gdb_process.write(command.encode() + b'\n')
        else:
            QMessageBox.warning(self.parent, "Warnung", "Debugger läuft nicht.")
