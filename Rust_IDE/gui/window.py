# window.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTextEdit, QSplitter, QFileDialog, QMessageBox
from PyQt5.QtCore import QProcess, Qt
from gui.widgets import create_menu_bar
from editor import RustEditor
from rust_integration import RustIntegration
from explorer import ProjectExplorer
from PyQt5.QtGui import QIcon
from subprocess import run
import os
from cargo_toml_manager import TomlManager
from ide_git import GitIntegration  # Hinzugefügt für Git-Integration
from codestral import CodestralCompletionPlugin
from layout import LayoutSettings  # Importiere die LayoutSettings

class RustIDEWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setze das Fenster-Icon
        icon_path = os.path.join('resources', 'icons', 'project_icon.ico')
        self.setWindowIcon(QIcon(icon_path))

        self.setWindowTitle("Rust IDE")
        self.setGeometry(300, 300, 1000, 600)  # Fenstergröße erweitert


        # RustIntegration für Build/Run/Debug
        self.rust_integration = RustIntegration(self)

        # Git-Integration
        self.git_integration = GitIntegration(self)  # Git-Integration wird hier initialisiert

        # Editor mit Syntax-Highlighting
        self.editor = RustEditor()
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)

        # Projekt-Explorer initialisieren
        self.project_explorer = ProjectExplorer(self)
        self.project_explorer.setVisible(False)  # Explorer ist standardmäßig ausgeblendet

        # Erster Splitter für Projekt-Explorer (links) und Editor (rechts)
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.project_explorer)  # Füge den Projekt-Explorer hinzu
        main_splitter.addWidget(self.editor)
        main_splitter.setStretchFactor(0, 1)  # Linkes Widget (Explorer) kann schmaler sein
        main_splitter.setStretchFactor(1, 4)  # Rechtes Widget (Editor) nimmt mehr Platz ein

        # Zweiter Splitter für Editor (oben) und Ausgabe (unten)
        vertical_splitter = QSplitter(Qt.Vertical)
        vertical_splitter.addWidget(main_splitter)  # Füge den ersten Splitter hinzu (enthält Projekt-Explorer und Editor)
        vertical_splitter.addWidget(self.output_area)  # Füge die Ausgabe hinzu
        vertical_splitter.setStretchFactor(0, 4)  # Editor + Explorer nehmen mehr Platz ein
        vertical_splitter.setStretchFactor(1, 1)  # Ausgabe nimmt weniger Platz ein

        # Hauptlayout
        layout = QVBoxLayout()
        layout.addWidget(vertical_splitter)  # Füge den vertikalen Splitter hinzu
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Layout-Einstellungen
        self.layout_settings = LayoutSettings(self)

        # Menüleiste erstellen
        create_menu_bar(self)
        # Hier initialisieren wir das Codestral-Plugin
        self.codestral_plugin = CodestralCompletionPlugin(self)
        # self.codestral_plugin.initialize()


    def load_project(self, project_path):
        """Lade das Projekt und zeige den Explorer an."""
        try:
            if not os.path.exists(project_path):
                self.output_area.append(f"Projektpfad existiert nicht: {project_path}")
                QMessageBox.warning(self, "Fehler", "Projektpfad existiert nicht.")
                return

            self.project_explorer.load_project(project_path)
            self.project_explorer.setVisible(True)  # Projekt-Explorer anzeigen

            # Setze den Projektpfad in RustIntegration und lade die Cargo.toml
            self.rust_integration.project_path = project_path
            self.rust_integration.toml_manager = TomlManager(project_path, self.output_area)

            # Debugging: Ausgabe des geladenen Projektpfads
            print(f"Projektpfad erfolgreich gesetzt: {project_path}")

            # Git-Integration: Setze den Projektpfad
            self.git_integration.set_project_path(project_path)

            # Öffne die Cargo.toml Datei direkt nach dem Laden des Projekts
            cargo_toml_path = os.path.join(project_path, "Cargo.toml")
            if os.path.exists(cargo_toml_path):
                with open(cargo_toml_path, 'r', encoding='utf-8') as f:
                    cargo_data = f.read()
                    self.editor.setPlainText(cargo_data)
                    self.rust_integration.current_file = cargo_toml_path  # Setze den aktuellen Pfad zur Cargo.toml
                print(f"Cargo.toml Datei erfolgreich geladen: {cargo_toml_path}")
            else:
                QMessageBox.warning(self, "Fehler", "Cargo.toml Datei nicht gefunden.")
                print("Fehler: Cargo.toml Datei nicht gefunden.")
        
            self.output_area.append(f"Projekt {project_path} erfolgreich geladen.")
            print(f"Projektpfad: {project_path} geladen und Explorer sichtbar gemacht.")
        except Exception as e:
            print(f"Fehler beim Laden des Projekts: {e}")
            QMessageBox.critical(self, "Fehler", f"Fehler beim Laden des Projekts: {e}")




    # Funktion für 'cargo clean'
    def clean_project(self):
        """Funktion zum Bereinigen des Projekts (cargo clean)."""
        if self.rust_integration.project_path:
            # Debugging-Ausgabe
            self.output_area.append(f"Bereinige das Projekt: {self.rust_integration.project_path}")
            process = run(["cargo", "clean"], cwd=self.rust_integration.project_path, capture_output=True, text=True)
            self.output_area.setPlainText(process.stdout + process.stderr)
        else:
            self.output_area.setPlainText("Kein Projekt geöffnet.")

    # Funktion für 'gdb target/debug/Projektname'
    def start_gdb(self):
        if self.rust_integration.project_path:
            # Konstruiere den Pfad zur ausführbaren Datei korrekt
            executable_path = os.path.join(self.rust_integration.project_path, 'target', 'debug', 'Rust_Test')

            # Verwende QProcess anstelle von Popen, um gdb nicht zu blockieren
            self.gdb_process = QProcess(self)
            self.gdb_process.setProcessChannelMode(QProcess.MergedChannels)
            self.gdb_process.readyRead.connect(self.read_gdb_output)

            # Starte gdb
            self.gdb_process.start("gdb", [executable_path])

            if not self.gdb_process.waitForStarted():
                self.output_area.setPlainText("Fehler beim Starten von gdb")
        else:
            self.output_area.setPlainText("Kein Projekt geöffnet.")

    def read_gdb_output(self):
        # Lies die Ausgabe des gdb-Prozesses und schreibe sie in die output_area
        output = self.gdb_process.readAllStandardOutput().data().decode()
        self.output_area.append(output)
