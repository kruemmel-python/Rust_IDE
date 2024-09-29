# editor.py

from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QTextCursor
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QTextEdit

class RustEditor(QTextEdit):
    def __init__(self):
        super().__init__()        
        self.setPlainText("fn main() {\n    println!(\"Hello, World!\");\n}")
        self.highlighter = RustHighlighter(self.document())


    def highlight_text(self, text, fmt):
        """Markiere Text im Editor."""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)

        # Suchen des Textes und Anwenden des Formats
        while cursor.find(text):
            cursor.mergeCharFormat(fmt)

class RustHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Format für Schlüsselwörter
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0000FF"))  # Blau für Schlüsselwörter
        keyword_format.setFontWeight(QFont.Bold)

        keywords = [
            "\\bfn\\b", "\\blet\\b", "\\bmut\\b", "\\bif\\b", "\\belse\\b", 
            "\\bfor\\b", "\\bwhile\\b", "\\bloop\\b", "\\bimpl\\b", "\\bstruct\\b",
            "\\benum\\b", "\\btrait\\b", "\\bmatch\\b", "\\bconst\\b", "\\bmod\\b",
            "\\bpub\\b", "\\buse\\b", "\\bas\\b", "\\bextern\\b", "\\bcrate\\b"
        ]

        for keyword in keywords:
            self.highlighting_rules.append((QRegExp(keyword), keyword_format))

        # Format für Kommentare
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#008000"))  # Grün für Kommentare
        self.highlighting_rules.append((QRegExp("//[^\n]*"), comment_format))

        # Format für Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#BA2121"))  # Rot für Strings
        self.highlighting_rules.append((QRegExp("\".*\""), string_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)
