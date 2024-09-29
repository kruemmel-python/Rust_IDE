from PyQt5.QtWidgets import QColorDialog, QFontDialog, QInputDialog, QMessageBox
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QSettings

class LayoutSettings:
    def __init__(self, parent):
        self.parent = parent
        self.settings = QSettings("YourCompany", "YourApp")  # QSettings wird hier initialisiert
        self.load_settings()

    def load_settings(self):
        """Lädt die gespeicherten Einstellungen."""
        # Schriftarten und Schriftgrößen laden
        font_family = self.settings.value("font_family", self.parent.editor.font().family())
        font_size = self.settings.value("font_size", self.parent.editor.font().pointSize())
        font = QFont(font_family, font_size)
        self.parent.editor.setFont(font)
        self.parent.output_area.setFont(font)
        self.parent.project_explorer.setFont(font)
        self.parent.menuBar().setFont(font)

        # Hintergrundfarben laden
        editor_bg_color = self.settings.value("editor_bg_color", "#ffffff")
        self.parent.editor.setStyleSheet(f"background-color: {editor_bg_color};")
        output_bg_color = self.settings.value("output_bg_color", "#ffffff")
        self.parent.output_area.setStyleSheet(f"background-color: {output_bg_color};")
        explorer_bg_color = self.settings.value("explorer_bg_color", "#ffffff")
        self.parent.project_explorer.setStyleSheet(f"background-color: {explorer_bg_color};")
        window_bg_color = self.settings.value("window_bg_color", "#ffffff")
        self.parent.setStyleSheet(f"background-color: {window_bg_color};")

        # Textfarben laden
        editor_text_color = self.settings.value("editor_text_color", "#000000")
        self.parent.editor.setStyleSheet(f"color: {editor_text_color};")
        output_text_color = self.settings.value("output_text_color", "#000000")
        self.parent.output_area.setStyleSheet(f"color: {output_text_color};")
        explorer_text_color = self.settings.value("explorer_text_color", "#000000")
        self.parent.project_explorer.setStyleSheet(f"color: {explorer_text_color};")
        menu_text_color = self.settings.value("menu_text_color", "#000000")
        self.parent.menuBar().setStyleSheet(f"color: {menu_text_color};")

    def save_settings(self):
        """Speichert die aktuellen Einstellungen."""
        font = self.parent.editor.font()
        self.settings.setValue("font_family", font.family())
        self.settings.setValue("font_size", font.pointSize())

    def change_font(self):
        """Ändert die Schriftart und -größe für alle Bereiche."""
        font, ok = QFontDialog.getFont(self.parent.editor.font(), self.parent, "Schriftart wählen")
        if ok:
            self.parent.editor.setFont(font)
            self.parent.output_area.setFont(font)
            self.parent.project_explorer.setFont(font)
            self.parent.menuBar().setFont(font)
            self.parent.output_area.append(f"Schriftart geändert zu: {font.family()} mit Größe: {font.pointSize()}")
            self.save_settings()

    def change_font_size(self):
        """Ändert die Schriftgröße für den Editor, die Ausgabe und den Projekt-Explorer."""
        size, ok = QInputDialog.getInt(self.parent, "Schriftgröße wählen", "Größe:", value=self.parent.editor.font().pointSize(), min=8, max=72)
        if ok:
            font = self.parent.editor.font()
            font.setPointSize(size)
            self.parent.editor.setFont(font)
            self.parent.output_area.setFont(font)
            self.parent.project_explorer.setFont(font)
            self.parent.menuBar().setFont(font)
            self.parent.output_area.append(f"Schriftgröße geändert zu: {size}")
            self.save_settings()

    # Hintergrundfarben für verschiedene Bereiche
    def change_editor_bg_color(self):
        """Ändert die Hintergrundfarbe des Editors."""
        color = QColorDialog.getColor(initial=QColor("#ffffff"), title="Hintergrundfarbe des Editors wählen")
        if color.isValid():
            self.parent.editor.setStyleSheet(f"background-color: {color.name()};")
            self.settings.setValue("editor_bg_color", color.name())
            self.parent.output_area.append(f"Hintergrundfarbe des Editors geändert zu: {color.name()}")

    def change_output_bg_color(self):
        """Ändert die Hintergrundfarbe der Ausgabe."""
        color = QColorDialog.getColor(initial=QColor("#ffffff"), title="Hintergrundfarbe der Ausgabe wählen")
        if color.isValid():
            self.parent.output_area.setStyleSheet(f"background-color: {color.name()};")
            self.settings.setValue("output_bg_color", color.name())
            self.parent.output_area.append(f"Hintergrundfarbe der Ausgabe geändert zu: {color.name()}")

    def change_explorer_bg_color(self):
        """Ändert die Hintergrundfarbe des Projekt-Explorers."""
        color = QColorDialog.getColor(initial=QColor("#ffffff"), title="Hintergrundfarbe des Projekt-Explorers wählen")
        if color.isValid():
            self.parent.project_explorer.setStyleSheet(f"background-color: {color.name()};")
            self.settings.setValue("explorer_bg_color", color.name())
            self.parent.output_area.append(f"Hintergrundfarbe des Projekt-Explorers geändert zu: {color.name()}")

    def change_window_bg_color(self):
        """Ändert die Hintergrundfarbe des gesamten Fensters."""
        color = QColorDialog.getColor(initial=QColor("#ffffff"), title="Hintergrundfarbe des Fensters wählen")
        if color.isValid():
            self.parent.setStyleSheet(f"background-color: {color.name()};")
            self.settings.setValue("window_bg_color", color.name())
            self.parent.output_area.append(f"Hintergrundfarbe des Fensters geändert zu: {color.name()}")

    # Textfarben für verschiedene Bereiche
    def change_editor_text_color(self):
        """Ändert die Textfarbe des Editors."""
        color = QColorDialog.getColor(initial=QColor("#000000"), title="Textfarbe des Editors wählen")
        if color.isValid():
            self.parent.editor.setStyleSheet(f"color: {color.name()};")
            self.settings.setValue("editor_text_color", color.name())
            self.parent.output_area.append(f"Textfarbe des Editors geändert zu: {color.name()}")

    def change_output_text_color(self):
        """Ändert die Textfarbe der Ausgabe."""
        color = QColorDialog.getColor(initial=QColor("#000000"), title="Textfarbe der Ausgabe wählen")
        if color.isValid():
            self.parent.output_area.setStyleSheet(f"color: {color.name()};")
            self.settings.setValue("output_text_color", color.name())
            self.parent.output_area.append(f"Textfarbe der Ausgabe geändert zu: {color.name()}")

    def change_explorer_text_color(self):
        """Ändert die Textfarbe des Projekt-Explorers."""
        color = QColorDialog.getColor(initial=QColor("#000000"), title="Textfarbe des Projekt-Explorers wählen")
        if color.isValid():
            self.parent.project_explorer.setStyleSheet(f"color: {color.name()};")
            self.settings.setValue("explorer_text_color", color.name())
            self.parent.output_area.append(f"Textfarbe des Projekt-Explorers geändert zu: {color.name()}")

    def change_menu_text_color(self):
        """Ändert die Textfarbe der Menüleiste."""
        color = QColorDialog.getColor(initial=QColor("#000000"), title="Textfarbe der Menüleiste wählen")
        if color.isValid():
            self.parent.menuBar().setStyleSheet(f"color: {color.name()};")
            self.settings.setValue("menu_text_color", color.name())
            self.parent.output_area.append(f"Textfarbe der Menüleiste geändert zu: {color.name()}")

    def reset_to_default(self):
        """Setzt alle Layout-Einstellungen auf die Standardwerte zurück."""
        default_font = QFont("Arial", 12)
        self.parent.editor.setFont(default_font)
        self.parent.output_area.setFont(default_font)
        self.parent.project_explorer.setFont(default_font)
        self.parent.menuBar().setFont(default_font)

        # Standard Hintergrund- und Textfarben
        self.parent.editor.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.parent.output_area.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.parent.project_explorer.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.parent.setStyleSheet("background-color: #ffffff;")
        self.parent.menuBar().setStyleSheet("color: #000000;")

        self.settings.clear()
        self.parent.output_area.append("Alle Layout-Einstellungen wurden auf die Standardwerte zurückgesetzt.")
