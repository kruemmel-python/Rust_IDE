import subprocess
from PyQt5.QtWidgets import QAction
from plugins.plugin_interface import PluginInterface

class RustCodeFormatterPlugin(PluginInterface):
    def __init__(self, ide):
        self.ide = ide  # Speichern der IDE-Referenz
        self.action = QAction("Rust-Code formatieren", self.ide)
        self.action.triggered.connect(self.execute)

    def initialize(self):
        """Initialisierung des Plugins."""
        # Füge die Aktion zum existierenden "Code"-Menü hinzu, ohne ein neues Menü zu erstellen
        #self.ide.add_action_to_menu('Code', self.action)
        self.ide.log_to_output("Rust Code Formatter Plugin aktiviert.")

    def deinitialize(self):
        """Aufräumarbeiten des Plugins."""
        self.ide.remove_action_from_menu('Code', self.action)
        self.ide.log_to_output("Rust Code Formatter Plugin deaktiviert.")

    def execute(self):
        """Die Methode, die beim Ausführen des Plugins aufgerufen wird."""
        self.ide.log_to_output("Rust Code Formatter Plugin wird ausgeführt.")
        self.format_code()

    def format_code(self):
        """Formatiert den aktuellen Rust-Code mit rustfmt."""
        self.ide.log_to_output("Rust-Code wird formatiert...")

        # Prüfen, ob eine Datei im Editor geladen ist
        file_path = self.ide.rust_integration.current_file  # Aktuell geöffnete Datei aus der Rust-Integration

        if not file_path or not file_path.endswith('.rs'):
            self.ide.log_to_output("Keine Rust-Datei geladen oder zum Formatieren ausgewählt.")
            return

        self.ide.log_to_output(f"Formatiere Datei: {file_path}")

        try:
            # Ausführen von rustfmt auf der Datei
            result = subprocess.run(['rustfmt', file_path], capture_output=True, text=True)

            if result.returncode == 0:
                self.ide.log_to_output("Code erfolgreich formatiert.")
                # Aktualisiere den Editor-Inhalt nach der Formatierung
                with open(file_path, 'r', encoding='utf-8') as f:
                    formatted_code = f.read()
                    self.ide.editor.setPlainText(formatted_code)
            else:
                self.ide.log_to_output(f"Fehler beim Formatieren: {result.stderr}")
        except Exception as e:
            self.ide.log_to_output(f"Fehler beim Formatieren des Codes: {str(e)}")

# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return RustCodeFormatterPlugin(ide)
