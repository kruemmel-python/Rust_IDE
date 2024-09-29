import subprocess
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox
from PyQt5.QtCore import QObject, QProcess
from plugins.plugin_interface import PluginInterface

class ClippyPlugin(QObject, PluginInterface):
    def __init__(self, ide):
        super().__init__()
        self.ide = ide
        self.process = None

    def initialize(self):
        """Initialisiert das Plugin und erstellt das Clippy-Menü."""
        # Überprüfen, ob das Extras-Menü bereits existiert
        menu_bar = self.ide.menuBar()
        extras_menu = menu_bar.findChild(QMenu, "Extras")

        if not extras_menu:
            extras_menu = menu_bar.addMenu("Extras")
            extras_menu.setObjectName("Extras")

        # Clippy Untermenü erstellen
        clippy_menu = extras_menu.addMenu("Clippy")

        # Clippy-Überprüfung ausführen
        run_clippy_action = QAction("Clippy-Überprüfung ausführen", self.ide)
        run_clippy_action.triggered.connect(self.run_clippy)
        clippy_menu.addAction(run_clippy_action)

        # Hilfe-Untermenü hinzufügen
        help_action = QAction("Hilfe", self.ide)
        help_action.triggered.connect(self.show_help)
        clippy_menu.addAction(help_action)

    def run_clippy(self):
        """Führt den Clippy-Linter asynchron aus."""
        project_path = self.ide.rust_integration.project_path  # Annahme: Projektpfad in RustIntegration gespeichert
        if not project_path:
            QMessageBox.warning(self.ide, "Fehler", "Kein Projektpfad gefunden. Öffne zuerst ein Projekt.")
            return

        # QProcess verwenden, um Clippy asynchron auszuführen
        self.process = QProcess(self)
        self.process.setProgram("cargo")
        self.process.setArguments(["clippy"])
        self.process.setWorkingDirectory(project_path)

        # Verbinden der Ausgabe von Clippy mit der IDE-Ausgabekonsole
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

        # Starten des Prozesses
        self.process.start()

        # Ausgabe anzeigen, dass der Prozess gestartet wurde
        self.ide.output_area.append("Clippy-Überprüfung wird ausgeführt...")

    def handle_stdout(self):
        """Verarbeitet die Standardausgabe von Clippy."""
        output = self.process.readAllStandardOutput().data().decode()
        self.ide.output_area.append(output)

    def handle_stderr(self):
        """Verarbeitet die Fehlerausgabe von Clippy."""
        error_output = self.process.readAllStandardError().data().decode()
        self.ide.output_area.append(error_output)

    def process_finished(self):
        """Wird aufgerufen, wenn der Clippy-Prozess abgeschlossen ist."""
        self.ide.output_area.append("Clippy-Überprüfung abgeschlossen.")

    def show_help(self):
        """Zeigt eine kurze Information darüber, was Clippy macht."""
        QMessageBox.information(self.ide, "Clippy Hilfe", 
                                "Clippy ist ein Linter für Rust-Code, der Ihnen hilft, potenzielle Probleme "
                                "in Ihrem Code zu erkennen und zu beheben. Er analysiert den Code auf mögliche "
                                "Fehler, ineffiziente Strukturen und Best Practices.")

# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return ClippyPlugin(ide)
