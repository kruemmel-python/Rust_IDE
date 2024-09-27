# plugins/hover_plugin.py
from PyQt5.QtCore import QObject, QUrl, Qt
from PyQt5.QtWidgets import QToolTip, QMenu
from PyQt5.QtGui import QDesktopServices, QTextCursor
from plugins.plugin_interface import PluginInterface

class HoverPlugin(QObject, PluginInterface):
    def __init__(self, ide):
        super().__init__()
        self.ide = ide
        self.editor = ide.editor
        self.editor.setMouseTracking(True)
        self.editor.viewport().installEventFilter(self)

    def initialize(self):
        """Initialisierung des Plugins."""
        self.ide.log_to_output("Hover Plugin initialisiert.")
        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self.show_context_menu)

    def shutdown(self):
        """Aufräumarbeiten des Plugins."""
        self.ide.log_to_output("Hover Plugin deaktiviert.")
        self.editor.viewport().removeEventFilter(self)

    def eventFilter(self, source, event):
        """Überwacht Mausbewegungen, um Hover-Events zu behandeln."""
        if event.type() == event.MouseMove and source is self.editor.viewport():
            cursor = self.editor.cursorForPosition(event.pos())
            cursor.select(QTextCursor.WordUnderCursor)
            selected_text = cursor.selectedText()

            if selected_text:
                self.show_function_tooltip(event.globalPos(), selected_text)

        return super().eventFilter(source, event)

    def show_function_tooltip(self, global_position, function_name):
        """Zeigt ein Tooltip mit einem Link zur offiziellen Dokumentation auf docs.rs."""
        QToolTip.showText(global_position, f"Dokumentation für '{function_name}' verfügbar.\nRechtsklick für Optionen.")
       # self.ide.log_to_output(f"Tooltip für '{function_name}' angezeigt.")

    def show_context_menu(self, position):
        """Zeigt das Kontextmenü an, um die Dokumentation zu öffnen."""
        cursor = self.editor.cursorForPosition(position)
        cursor.select(QTextCursor.WordUnderCursor)
        selected_text = cursor.selectedText()

        if selected_text:
            # Erstelle das Kontextmenü
            context_menu = QMenu(self.editor)

            # Aktion für das Öffnen der Dokumentation
            docs_action = context_menu.addAction(f"Öffne Dokumentation für '{selected_text}' auf docs.rs")

            action = context_menu.exec_(self.editor.mapToGlobal(position))

            if action == docs_action:
                self.open_docs(selected_text)

    def open_docs(self, function_name):
        """Öffnet die Dokumentation der Funktion auf docs.rs."""
        # Erzeuge die URL für die Funktion auf docs.rs
        search_url = f"https://doc.rust-lang.org/std/?search={function_name}"
        QDesktopServices.openUrl(QUrl(search_url))
        self.ide.log_to_output(f"Dokumentation für '{function_name}' geöffnet.")

    def execute(self):
        """Diese Methode wird ausgeführt, wenn das Plugin aktiviert wird."""
        self.ide.log_to_output("Hover Plugin ausgeführt.")

# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return HoverPlugin(ide)
