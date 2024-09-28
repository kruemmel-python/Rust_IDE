import os
from PyQt5.QtWidgets import QAction, QTabWidget, QTextEdit
from PyQt5.QtCore import QProcess, QFileSystemWatcher, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Für die Vorschau
from plugins.plugin_interface import PluginInterface
import toml  # Bibliothek zum Parsen von TOML-Dateien


class DocumentationGeneratorPlugin(PluginInterface):
    def __init__(self, ide):
        self.ide = ide
        self.process = QProcess(self.ide)  # QProcess für asynchrone Prozessausführung
        self.action = QAction("Dokumentation generieren", self.ide)
        self.action.triggered.connect(self.execute)
        
        # Tab für die Dokumentationsvorschau erstellen
        self.doc_viewer = QWebEngineView()
        self.ide.tabs.addTab(self.doc_viewer, "Dokumentationsvorschau")

        # Dateiüberwachung für automatische Dokumentationserstellung
        self.watcher = QFileSystemWatcher()
        self.watcher.directoryChanged.connect(self.on_code_change)  # Überwache Code-Änderungen im Projektordner

    def initialize(self):
        """Initialisierung des Plugins."""
        self.ide.output_area.append("Documentation Generator Plugin aktiviert.")
        project_path = self.ide.rust_integration.project_path
        if project_path:
            # Verzeichnisse für die Überwachung hinzufügen
            self.watcher.addPath(project_path)

    def deinitialize(self):
        """Aufräumarbeiten des Plugins."""
        self.ide.output_area.append("Documentation Generator Plugin deaktiviert.")
    
    def get_project_name(self):
        """Liest den Projektnamen aus der Cargo.toml-Datei."""
        cargo_toml_path = os.path.join(self.ide.rust_integration.project_path, "Cargo.toml")
        if os.path.exists(cargo_toml_path):
            with open(cargo_toml_path, 'r', encoding='utf-8') as f:
                cargo_data = toml.load(f)
                return cargo_data.get("package", {}).get("name", None)
        return None
    
    def generate_docs(self):
        """Asynchrone Generierung der Dokumentation für das Rust-Projekt mit 'cargo doc'."""
        project_path = self.ide.rust_integration.project_path
        if not project_path:
            self.ide.output_area.append("Fehler: Kein Projektpfad gefunden.")
            return

        self.ide.output_area.append(f"Dokumentation wird für das Projekt im Pfad {project_path} generiert...")

        # Prozessausgabe überwachen und anzeigen
        self.process.setProgram("cargo")
        self.process.setArguments(["doc", "--no-deps"])
        self.process.setWorkingDirectory(project_path)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        
        # Starte den Prozess
        self.process.start()

    def handle_stdout(self):
        """Liest und gibt die Standardausgabe des Prozesses aus."""
        output = self.process.readAllStandardOutput().data().decode()
        self.ide.output_area.append(output)

    def handle_stderr(self):
        """Liest und gibt die Standardfehlerausgabe des Prozesses aus."""
        error_output = self.process.readAllStandardError().data().decode()
        self.ide.output_area.append(error_output)

    def process_finished(self):
        """Wird aufgerufen, wenn der Prozess abgeschlossen ist."""
        self.ide.output_area.append("Dokumentation erfolgreich generiert.")
    
        # Den Projektnamen dynamisch ermitteln
        project_name = self.get_project_name()
        if project_name is None:
            self.ide.output_area.append("Fehler: Projektnamen konnte nicht ermittelt werden.")
            return

        # Korrektes Verzeichnis für die Dokumentation, basierend auf dem Projektnamen
        doc_index_path = os.path.join(self.ide.rust_integration.project_path, "target", "doc", project_name, "index.html")
    
        if os.path.exists(doc_index_path):
            # Konvertiere den Pfad zu einem QUrl-Objekt
            url = QUrl.fromLocalFile(doc_index_path)
            # Lade die HTML-Datei in den WebViewer
            self.doc_viewer.load(url)
            self.ide.output_area.append("Dokumentation wird im Vorschau-Tab angezeigt.")
        else:
            # Fehleranzeige, wenn der Dokumentationsindex nicht gefunden wird
            self.ide.output_area.append(f"Fehler: Dokumentationsindex nicht gefunden unter {doc_index_path}.")

    def on_code_change(self, path):
        """Wird aufgerufen, wenn eine Änderung im Projektverzeichnis erkannt wird."""
        self.ide.output_area.append(f"Änderung im Projekt erkannt. Generiere Dokumentation neu...")
        self.generate_docs()  # Dokumentation automatisch neu generieren
    
    def execute(self):
        """Die Methode wird aufgerufen, wenn das Plugin im Menü ausgewählt wird."""
        self.ide.output_area.append("Documentation Generator Plugin wurde ausgeführt.")
        self.generate_docs()

# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return DocumentationGeneratorPlugin(ide)
