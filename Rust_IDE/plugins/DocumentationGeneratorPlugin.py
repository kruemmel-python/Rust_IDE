# plugins/DocumentationGeneratorPlugin.py
import os
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QProcess
from plugins.plugin_interface import PluginInterface

class DocumentationGeneratorPlugin(PluginInterface):
    def __init__(self, ide):
        self.ide = ide
        self.process = QProcess(self.ide)  # QProcess für asynchrone Prozessausführung
        self.action = QAction("Dokumentation generieren", self.ide)
        self.action.triggered.connect(self.execute)

    def initialize(self):
        """Initialisierung des Plugins."""
        self.ide.output_area.append("Documentation Generator Plugin aktiviert.")
    
    def deinitialize(self):
        """Aufräumarbeiten des Plugins."""
        self.ide.output_area.append("Documentation Generator Plugin deaktiviert.")
    
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
    
    def execute(self):
        """Die Methode wird aufgerufen, wenn das Plugin im Menü ausgewählt wird."""
        self.ide.output_area.append("Documentation Generator Plugin wurde ausgeführt.")
        self.generate_docs()

# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return DocumentationGeneratorPlugin(ide)
