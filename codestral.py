import requests
import pyperclip
from PyQt5.QtWidgets import QAction, QMessageBox

class CodestralCompletionPlugin:
    def __init__(self, ide):
        self.ide = ide
        self.action = QAction("Code vervollständigen", self.ide)
        self.action.triggered.connect(self.complete_code)

    def initialize(self):
        # Füge die Aktion "Code vervollständigen" zum Menü hinzu
        self.ide.menuBar().addAction(self.action)
        self.ide.output_area.append("Codestral Completion Plugin aktiviert.")

    def deinitialize(self):
        # Entferne die Aktion aus dem Menü
        self.ide.menuBar().removeAction(self.action)
        self.ide.output_area.append("Codestral Completion Plugin deaktiviert.")

    def complete_code(self):
        self.ide.output_area.append("Code-Vervollständigung wird ausgeführt...")

        # Hole den gesamten Code aus dem Editor
        code = self.ide.editor.toPlainText()

        # Wenn der Code nicht leer ist, mache die API-Anfrage
        if code:
            try:
                # Dein API-Schlüssel
                API_KEY = "gzJqoKln4xPgTKO7xE15MhjX0fzrSA6i"
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "codestral-latest",  # Das richtige Modell verwenden
                    "messages": [
                        {"role": "system", "content": "Du bist ein hilfreicher Rust Leher für die Codevervollständigung."},
                        {"role": "user", "content": f"Vervollständige den folgenden Code:\n\n{code}"}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                }

                # Anfrage an die API
                response = requests.post(
                    "https://codestral.mistral.ai/v1/chat/completions", 
                    headers=headers, 
                    json=data
                )

                # Verarbeite die API-Antwort
                if response.status_code == 200:
                    completion = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                    if completion:
                        self.ide.output_area.append(f"Vervollständigung: {completion}")
                        pyperclip.copy(completion)
                        self.ide.output_area.append("Vervollständigung in die Zwischenablage kopiert.")
                        # Füge die Vervollständigung in den Editor ein
                        self.insert_completion(completion)
                    else:
                        self.ide.output_area.append("Keine Vervollständigung erhalten.")
                else:
                    self.ide.output_area.append(f"Fehler: {response.status_code} - {response.text}")
            except Exception as e:
                self.ide.output_area.append(f"Fehler bei der Anfrage: {str(e)}")
        else:
            self.ide.output_area.append("Kein Code zum Vervollständigen vorhanden.")

    def insert_completion(self, completion):
        # Erhalte den aktuellen Textcursor
        cursor = self.ide.editor.textCursor()
    
        # Füge den vervollständigten Text an der aktuellen Cursor-Position ein
        cursor.insertText(completion)
    
        # Setze den Cursor nach der eingefügten Vervollständigung
        self.ide.editor.setTextCursor(cursor)


def create_plugin(ide):
    return CodestralCompletionPlugin(ide)
