# plugins/UnittestPlugin.py
import os
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QProcess
from plugins.plugin_interface import PluginInterface

class UnittestPlugin(PluginInterface):
    def __init__(self, ide):
        self.ide = ide
        self.process = QProcess(self.ide)  # QProcess für asynchrone Prozessausführung
        self.action = QAction("Unittests ausführen", self.ide)
        self.action.triggered.connect(self.execute)

    def initialize(self):
        """Initialisierung des Plugins."""
        self.ide.output_area.append("Unittest Plugin aktiviert.")
    
    def deinitialize(self):
        """Aufräumarbeiten des Plugins."""
        self.ide.output_area.append("Unittest Plugin deaktiviert.")
    
    def run_tests(self):
        """Asynchrone Ausführung von Rust-Unittests mit 'cargo test'."""
        project_path = self.ide.rust_integration.project_path
        if not project_path:
            self.ide.output_area.append("Fehler: Kein Projektpfad gefunden.")
            return

        self.ide.output_area.append(f"Unittests werden für das Projekt im Pfad {project_path} ausgeführt...")

        # Prozessausgabe überwachen und anzeigen
        self.process.setProgram("cargo")
        self.process.setArguments(["test"])
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
        self.ide.output_area.append("Unittests abgeschlossen.")
    
    def execute(self):
        """Die Methode wird aufgerufen, wenn das Plugin im Menü ausgewählt wird."""
        self.ide.output_area.append("Unittest Plugin wurde ausgeführt.")
        self.run_tests()

# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return UnittestPlugin(ide)
