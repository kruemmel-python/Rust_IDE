from PyQt5.QtWidgets import QFontDialog, QAction, QInputDialog
from PyQt5.QtGui import QFont

class LayoutSettings:
    def __init__(self, parent):
        self.parent = parent
        self.default_font = parent.editor.font()  # Standard-Schriftart aus dem Editor übernehmen

    def change_font(self):
        """Öffnet einen Dialog zur Auswahl der Schriftart."""
        font, ok = QFontDialog.getFont(self.default_font, self.parent, "Schriftart wählen")
        if ok:
            self.parent.editor.setFont(font)
            self.parent.output_area.append(f"Schriftart geändert zu: {font.family()}")

    def change_font_size(self):
        """Öffnet einen Dialog zur Eingabe der Schriftgröße."""
        size, ok = QInputDialog.getInt(self.parent, "Schriftgröße wählen", "Größe:", value=self.default_font.pointSize(), min=8, max=72)
        if ok:
            font = self.parent.editor.font()
            font.setPointSize(size)
            self.parent.editor.setFont(font)
            self.parent.output_area.append(f"Schriftgröße geändert zu: {size}")
