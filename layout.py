from PyQt5.QtWidgets import QFontDialog, QAction, QInputDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSettings

class LayoutSettings:
    def __init__(self, parent):
        self.parent = parent
        self.settings = QSettings("YourCompany", "YourApp")  # Ersetze "YourCompany" und "YourApp" durch deine eigenen Werte
        self.load_settings()

    def load_settings(self):
        """Lädt die gespeicherten Einstellungen."""
        font_family = self.settings.value("font_family", self.parent.editor.font().family())
        font_size = self.settings.value("font_size", self.parent.editor.font().pointSize())
        font = QFont(font_family, font_size)
        self.parent.editor.setFont(font)
        self.parent.output_area.setFont(font)
        self.parent.project_explorer.setFont(font)

    def save_settings(self):
        """Speichert die aktuellen Einstellungen."""
        font = self.parent.editor.font()
        self.settings.setValue("font_family", font.family())
        self.settings.setValue("font_size", font.pointSize())

    def change_font(self):
        """Öffnet einen Dialog zur Auswahl der Schriftart."""
        font, ok = QFontDialog.getFont(self.parent.editor.font(), self.parent, "Schriftart wählen")
        if ok:
            # Setze die Schriftart für den Editor, die Ausgabe und den Projekt-Explorer
            self.parent.editor.setFont(font)
            self.parent.output_area.setFont(font)
            self.parent.project_explorer.setFont(font)
            self.parent.output_area.append(f"Schriftart geändert zu: {font.family()}")
            self.save_settings()

    def change_font_size(self):
        """Öffnet einen Dialog zur Eingabe der Schriftgröße."""
        size, ok = QInputDialog.getInt(self.parent, "Schriftgröße wählen", "Größe:", value=self.parent.editor.font().pointSize(), min=8, max=72)
        if ok:
            # Setze die Schriftgröße für den Editor, die Ausgabe und den Projekt-Explorer
            font = self.parent.editor.font()
            font.setPointSize(size)
            self.parent.editor.setFont(font)
            self.parent.output_area.setFont(font)
            self.parent.project_explorer.setFont(font)
            self.parent.output_area.append(f"Schriftgröße geändert zu: {size}")
            self.save_settings()
