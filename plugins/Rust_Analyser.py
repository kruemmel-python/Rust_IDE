import re
from PyQt5.QtCore import QThread, pyqtSignal, QRegExp
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor, QTextCursor
from PyQt5.QtWidgets import QAction, QMessageBox
import subprocess
from plugins.plugin_interface import PluginInterface

class RustAnalyzerThread(QThread):
    # Signal, um das Ergebnis oder den Status zurückzugeben
    finished = pyqtSignal(str)

    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path

    def run(self):
        try:
            # Führe cargo check aus, um den Code zu überprüfen
            process = subprocess.Popen(
                ["cargo", "check"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_path  # Setze das Projektverzeichnis als Arbeitsverzeichnis
            )
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                self.finished.emit(f"Rust Analyzer erfolgreich abgeschlossen:\n{stdout}")
            else:
                self.finished.emit(f"Fehler beim Ausführen von cargo check:\n{stderr}")
        except Exception as e:
            self.finished.emit(f"Fehler: {str(e)}")

class RustAnalyzerPlugin(PluginInterface):
    def __init__(self, ide):
        self.ide = ide
        self.thread = None

    def initialize(self):
        """Initialisiert das Plugin und erstellt das Rust Analyzer-Menü."""
        # Prüfen, ob das Menü 'Extras' schon existiert
        extras_menu = None
        for menu in self.ide.menuBar().actions():
            if menu.text() == "Extras":
                extras_menu = menu.menu()
                break

        if not extras_menu:
            extras_menu = self.ide.menuBar().addMenu("Extras")

        # Menüpunkt für den Rust Analyzer hinzufügen
        analyzer_action = QAction("Rust Analyzer starten", self.ide)
        analyzer_action.triggered.connect(self.run_rust_analyzer)
        extras_menu.addAction(analyzer_action)

    def run_rust_analyzer(self):
        """Startet den Rust Analyzer in einem separaten Thread."""
        project_path = self.get_project_path()
        if not project_path:
            QMessageBox.warning(self.ide, "Fehler", "Kein Projekt geöffnet.")
            return

        # Rust Analyzer für das aktuelle Projekt starten
        self.thread = RustAnalyzerThread(project_path)
        self.thread.finished.connect(self.on_rust_analyzer_finished)
        self.thread.start()

        self.ide.output_area.append(f"Rust Analyzer wird für Projekt {project_path} ausgeführt...")

    def on_rust_analyzer_finished(self, result):
        """Behandelt das Ergebnis des Rust Analyzers."""
        self.ide.output_area.append(result)  # Ausgabe im Output-Fenster

        # Analysiere den Output, um Fehlerpositionen zu finden
        errors = self.parse_rust_analyzer_output(result)

        # Fehler im Editor hervorheben
        self.highlight_errors_in_editor(errors)

    def parse_rust_analyzer_output(self, output):
        """Extrahiere Fehler und Warnungen aus dem Rust Analyzer Output."""
        errors = []
        # Nutze Regex, um Fehler- und Warnungsmeldungen zu extrahieren
        error_pattern = re.compile(r'error.*? --> (.*?):(\d+):(\d+)')
        warning_pattern = re.compile(r'warning.*? --> (.*?):(\d+):(\d+)')
        
        for line in output.splitlines():
            error_match = error_pattern.search(line)
            warning_match = warning_pattern.search(line)
            if error_match:
                file_path, line_num, col_num = error_match.groups()
                errors.append((file_path, int(line_num), int(col_num), "error"))
            elif warning_match:
                file_path, line_num, col_num = warning_match.groups()
                errors.append((file_path, int(line_num), int(col_num), "warning"))
        
        return errors


    def highlight_errors_in_editor(self, errors):
        """
        Hebt die Fehler im Editor hervor, indem ein gelbes Rechteck um den fehlerhaften Code gelegt wird.
        """
        cursor = self.ide.editor.textCursor()
        format = QTextCharFormat()
        format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        format.setUnderlineColor(QColor("yellow"))
    
        # Setze die Fehler im Editor zurück, indem alle Markierungen entfernt werden
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())  # Entfernt alle bestehenden Formate
    
        # Suche und markiere die Fehlerstellen
        for error in errors:
            # Angenommen, der Fehler gibt die Zeile und den fehlerhaften Text an
            # Du musst den Fehlertext hier extrahieren (zum Beispiel mit einer regex oder einem Parser)
            line_number, error_text = self.extract_error_details(error)
        
            if line_number is not None and error_text:
                # Setze den Cursor auf die fehlerhafte Zeile
                cursor.movePosition(QTextCursor.Start)
                for _ in range(line_number - 1):
                    cursor.movePosition(QTextCursor.Down)
            
                # Suche den Fehlertext in der Zeile und markiere ihn
                cursor.select(QTextCursor.LineUnderCursor)
                line_text = cursor.selectedText()
            
                # Finde den Fehlertext in der Zeile
                start_index = line_text.find(error_text)
                if start_index != -1:
                    cursor.setPosition(cursor.position() + start_index)
                    cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(error_text))
                
                    # Setze das gelbe Umrandungsformat
                    cursor.setCharFormat(format)
    
        self.ide.output_area.append("Fehler wurden im Editor hervorgehoben.")
    

    def extract_error_details(self, error):
        """
        Extrahiert die Zeile und den fehlerhaften Text aus einer Fehlernachricht.
        """
        # Beispiel für Fehlerverarbeitung: Extrahiere die Zeile und den Fehlertext
        match = re.search(r"--> src/(.*):(\d+):(\d+)", error)
        if match:
            line_number = int(match.group(2))
            error_text = "pintln"  # Beispiel: dies sollte aus dem Fehlerlog extrahiert werden
            return line_number, error_text
        return None, None

    def get_project_path(self):
        """Gibt den Pfad des Projekts zurück, in dem sich die Cargo.toml-Datei befindet."""
        file_path = self.ide.rust_integration.current_file
        if file_path:
            # Gehe davon aus, dass das Projektverzeichnis die `Cargo.toml` enthält
            project_path = file_path.rsplit("/src/", 1)[0]
            return project_path
        return None

    def shutdown(self):
        """Aufräumarbeiten beim Schließen des Plugins."""
        pass

# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return RustAnalyzerPlugin(ide)
