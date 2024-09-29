import requests
import pyperclip
from PyQt5.QtCore import QUrl, QObject, Qt
from PyQt5.QtWidgets import QToolTip, QMenu, QDialog, QVBoxLayout, QTextEdit, QPushButton, QScrollArea, QWidget, QAction, QSpinBox, QLabel, QHBoxLayout
from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from plugins.plugin_interface import PluginInterface


class HoverWithQuickfixPlugin(QObject, PluginInterface):
    def __init__(self, ide):
        super().__init__()
        self.ide = ide
        self.editor = ide.editor
        self.editor.setMouseTracking(True)
        self.editor.viewport().installEventFilter(self)
        self.font_size = 14  # Standard-Schriftgröße

    def initialize(self):
        """Initialisierung des Plugins."""
        self.ide.output_area.append("Hover with Quickfix Plugin initialisiert.")
        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self.show_context_menu)

    def shutdown(self):
        """Aufräumarbeiten des Plugins."""
        self.ide.output_area.append("Hover with Quickfix Plugin deaktiviert.")
        self.editor.viewport().removeEventFilter(self)

    def execute(self):
        """Die erforderliche Methode, die aus dem PluginInterface implementiert wird."""
        self.ide.output_area.append("HoverWithQuickfixPlugin ausgeführt!")

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
        """Zeigt ein Tooltip mit einem Link zur offiziellen Dokumentation oder Beispielcode."""
        QToolTip.showText(global_position, f"{function_name} - Rechtsklick für Beispiel und Erklärung.")

    def show_context_menu(self, position):
        """Zeigt das Kontextmenü an, um Quickfix-Optionen anzubieten."""
        cursor = self.editor.textCursor()  # Verwende den TextCursor, um den gesamten markierten Text zu erhalten
        selected_text = cursor.selectedText().strip()  # Entferne eventuelle Leerzeichen um den Text

        if selected_text:
            context_menu = QMenu(self.editor)

            # Quickfix Aktion, um ein Beispiel und eine Erklärung für den markierten Text anzuzeigen
            quickfix_action = context_menu.addAction(f"Beispiel und Erklärung für '{selected_text}' über Codestral")

            # Menü für Schriftgrößenänderung
            font_menu = context_menu.addMenu("Schriftgröße ändern")
            increase_font_action = font_menu.addAction("Größer")
            decrease_font_action = font_menu.addAction("Kleiner")

            action = context_menu.exec_(self.editor.mapToGlobal(position))

            if action == quickfix_action:
                self.run_quickfix(selected_text)  # Den markierten Text als Argument übergeben
            elif action == increase_font_action:
                self.change_font_size(2)
            elif action == decrease_font_action:
                self.change_font_size(-2)

    def change_font_size(self, adjustment):
        """Ändert die Schriftgröße des Textfeldes im Dialog."""
        self.font_size = max(8, self.font_size + adjustment)  # Begrenze die minimale Schriftgröße auf 8
        self.ide.output_area.append(f"Schriftgröße geändert: {self.font_size}pt")

    def run_quickfix(self, selected_text):
        """Führt den Quickfix über die Codestral Chat-API aus und zeigt das Beispiel und die Erklärung an."""

        if not selected_text:
            # Wenn kein Text markiert wurde, gib eine Warnung aus
            self.ide.output_area.append("Kein Text ausgewählt. Bitte markiere einen Textbereich.")
            return

        self.ide.output_area.append(f"Beispiel und Erklärung für den markierten Text:\n'{selected_text}' werden über Codestral angefordert...")

        API_KEY = "gzJqoKln4xPgTKO7xE15MhjX0fzrSA6i"  # Dein API-Schlüssel
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "codestral-latest",  # Das richtige Modell verwenden
            "messages": [
                {
                    "role": "system",
                    "content": "Du bist ein hilfsbereiter deutsch sprechender Lehrer, der Rust-Code mit Erklärung erstellt."
                },
                {
                    "role": "user",
                    "content": f"Schreibe ein einfaches Rust-Code-Beispiel basierend auf diesem markierten Text: '{selected_text}' und erkläre kurz, wie es funktioniert, und das immer in Deutsch."
                }
            ],
            "max_tokens": 500,
            "temperature": 0.2
        }

        try:
            response = requests.post(
                "https://codestral.mistral.ai/v1/chat/completions",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                response_json = response.json()

                # Überprüfen, ob "choices" im JSON enthalten ist
                if "choices" in response_json and isinstance(response_json["choices"], list) and response_json["choices"]:
                    message = response_json["choices"][0].get("message", {}).get("content", "")
                    if message:
                        self.show_completion_dialog(message)
                    else:
                        self.ide.output_area.append("Keine gültige 'message' erhalten.")
                else:
                    self.ide.output_area.append("Die Antwort enthält keine gültigen 'choices'.")
            else:
                self.ide.output_area.append(f"Fehler: HTTP {response.status_code} - {response.text}")
        except Exception as e:
            self.ide.output_area.append(f"Fehler bei der Anfrage: {str(e)}")

    def show_completion_dialog(self, completion):
        """Zeigt das Beispiel und die Erklärung in einem Dialog an."""
        dialog = QDialog(self.ide)
        dialog.setWindowTitle("Beispiel und Erklärung")

        # Setze die feste Fenstergröße
        dialog.setFixedSize(800, 600)  # Beispiel: Fenstergröße 800x600 Pixel

        layout = QVBoxLayout()

        text_edit = QTextEdit(dialog)
        text_edit.setPlainText(completion)

        # Setze die Standard-Schriftgröße
        font = QFont()
        font.setPointSize(self.font_size)
        text_edit.setFont(font)
        layout.addWidget(text_edit)

        # Hinzufügen einer SpinBox für die Schriftgrößenänderung
        font_size_label = QLabel("Schriftgröße:")
        font_size_spinbox = QSpinBox()
        font_size_spinbox.setRange(8, 48)  # Festlegen des Größenbereichs
        font_size_spinbox.setValue(self.font_size)
        font_size_spinbox.valueChanged.connect(lambda value: self.change_font_size_for_text_edit(text_edit, value))

        # Horizontaler Layout für die SpinBox und das Label
        font_layout = QHBoxLayout()
        font_layout.addWidget(font_size_label)
        font_layout.addWidget(font_size_spinbox)
        layout.addLayout(font_layout)

        # Buttons
        insert_button = QPushButton("Text kopieren", dialog)
        cancel_button = QPushButton("Schließen", dialog)
        layout.addWidget(insert_button)
        layout.addWidget(cancel_button)

        dialog.setLayout(layout)

        insert_button.clicked.connect(lambda: self.copy_to_clipboard(completion))
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec_()

    def change_font_size_for_text_edit(self, text_edit, size):
        """Ändert die Schriftgröße im Textfeld."""
        font = text_edit.font()
        font.setPointSize(size)
        text_edit.setFont(font)
        self.font_size = size  # Aktualisiere die Schriftgröße für zukünftige Dialoge

    def copy_to_clipboard(self, text):
        """Kopiert den Text in die Zwischenablage."""
        pyperclip.copy(text)
        self.ide.output_area.append("Beispiel und Erklärung in die Zwischenablage kopiert.")
