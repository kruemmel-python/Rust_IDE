# plugins/refactor_plugin.py
from plugins.plugin_interface import PluginInterface
from PyQt5.QtWidgets import QAction, QInputDialog

class RefactorPlugin(PluginInterface):
    def __init__(self, ide):
        # Speichere die IDE-Referenz
        self.ide = ide
        # Erstelle die Refactoring-Aktion
        self.action = QAction('Code Refactoring', self.ide)
        self.action.setShortcut('Ctrl+Shift+R')
        self.action.triggered.connect(self.refactor_code)

    def initialize(self):
        """Initialisierung des Plugins."""
        # Füge die Aktion zum existierenden "Code"-Menü hinzu, ohne ein neues Menü zu erstellen
       # self.ide.add_action_to_menu('Code', self.action)
        self.ide.log_to_output("Refactor Plugin aktiviert.")

    def deinitialize(self):
        """Aufräumarbeiten des Plugins."""
        self.ide.remove_action_from_menu('Code', self.action)
        self.ide.log_to_output("Refactoring Plugin deaktiviert.")  # Ausgabe in der Konsole

    def refactor_code(self):
        """Führt das Code-Refactoring durch."""
        self.ide.log_to_output("Code Refactoring wird ausgeführt...")

        cursor = self.ide.editor.textCursor()
        selected_text = cursor.selectedText()

        if not selected_text:
            self.ide.log_to_output("Kein Text ausgewählt zum Refaktorisieren.")
            return

        new_name, ok = QInputDialog.getText(self.ide, 'Code Refactoring', f'Ersetzen "{selected_text}" durch:')
        if ok and new_name:
            # Refactoring im gesamten Code durchführen
            code = self.ide.editor.toPlainText()
            updated_code = code.replace(selected_text, new_name)
            self.ide.editor.setPlainText(updated_code)
            self.ide.log_to_output(f'"{selected_text}" wurde im gesamten Code durch "{new_name}" ersetzt.')
        else:
            self.ide.log_to_output("Refaktorisieren abgebrochen.")

# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return RefactorPlugin(ide)