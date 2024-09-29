# explorer.py
import os
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QMenu, QAction, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt

class ProjectExplorer(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.model = QFileSystemModel()
        self.setModel(self.model)
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Kontextmenü aktivieren
        self.customContextMenuRequested.connect(self.open_context_menu)  # Kontextmenü öffnen
        self.doubleClicked.connect(self.open_file_in_editor)  # Datei per Doppelklick im Editor öffnen

    def load_project(self, project_path):
        """Lade die Verzeichnisstruktur des Projekts in den Explorer."""
        if not os.path.exists(project_path):
            self.parent.output_area.append(f"Projektpfad existiert nicht: {project_path}")
            return
        
        # Debugging-Ausgabe
        print(f"Verzeichnisstruktur wird geladen für Projektpfad: {project_path}")

        self.model.setRootPath(project_path)  # Root des Modells auf das Projekt setzen
        self.setRootIndex(self.model.index(project_path))
        self.parent.output_area.append(f"Projekt {project_path} geladen.")
    
    def open_context_menu(self, position):
        """Öffne das Kontextmenü mit Rechtsklick."""
        index = self.indexAt(position)
        if not index.isValid():
            return

        file_path = self.model.filePath(index)
        menu = QMenu()

        # Optionen für Dateien und Ordner
        if os.path.isfile(file_path):
            delete_action = QAction("Datei löschen", self)
            delete_action.triggered.connect(lambda: self.delete_item(file_path))
            menu.addAction(delete_action)
        else:
            new_file_action = QAction("Neue Datei erstellen", self)
            new_file_action.triggered.connect(lambda: self.create_file(file_path))
            menu.addAction(new_file_action)

            new_folder_action = QAction("Neuen Ordner erstellen", self)
            new_folder_action.triggered.connect(lambda: self.create_folder(file_path))
            menu.addAction(new_folder_action)

            delete_folder_action = QAction("Ordner löschen", self)
            delete_folder_action.triggered.connect(lambda: self.delete_item(file_path))
            menu.addAction(delete_folder_action)

        menu.exec_(self.viewport().mapToGlobal(position))

    def open_file_in_editor(self, index):
        """Öffne die ausgewählte Datei oder lade das Projekt, falls ein Ordner ausgewählt ist."""
        file_path = self.model.filePath(index)
    
        # Wenn es sich um eine Datei handelt, öffne sie im Editor
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.parent.editor.setPlainText(content)
                    self.parent.rust_integration.current_file = file_path  # Setzt die aktuelle Datei
                self.parent.output_area.append(f"Datei {file_path} im Editor geöffnet.")
            except Exception as e:
                self.parent.output_area.append(f"Fehler beim Öffnen der Datei {file_path}: {e}")
    
        # Wenn es sich um einen Ordner handelt, überprüfe, ob es sich um ein Rust-Projekt handelt
        elif os.path.isdir(file_path):
            cargo_toml_path = os.path.join(file_path, 'Cargo.toml')
            if os.path.exists(cargo_toml_path):
                self.parent.load_project(file_path)  # Lade das Projekt und die main.rs
            else:
                self.parent.output_area.append(f"Kein Cargo.toml in {file_path} gefunden.")




    def create_file(self, folder_path):
        """Erstelle eine neue Datei in dem ausgewählten Ordner."""
        if not os.path.isdir(folder_path):
            QMessageBox.warning(self, "Fehler", "Bitte wählen Sie einen gültigen Ordner aus.")
            return

        file_name, ok = QInputDialog.getText(self, "Neue Datei", "Dateiname eingeben:")
        if ok and file_name:
            full_path = os.path.join(folder_path, file_name)
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    pass  # Leere Datei erstellen
                self.parent.output_area.append(f"Datei {full_path} erstellt.")
                self.model.refresh()  # Modell aktualisieren
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Konnte Datei nicht erstellen: {e}")


    def create_folder(self, folder_path):
        """Erstelle einen neuen Ordner im ausgewählten Ordner."""
        if not os.path.isdir(folder_path):
            QMessageBox.warning(self, "Fehler", "Bitte wählen Sie einen gültigen Ordner aus.")
            return

        folder_name, ok = QInputDialog.getText(self, "Neuer Ordner", "Ordnername eingeben:")
        if ok and folder_name:
            full_path = os.path.join(folder_path, folder_name)
            try:
                os.makedirs(full_path)
                self.parent.output_area.append(f"Ordner {full_path} erstellt.")
                self.model.refresh()  # Modell aktualisieren
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Konnte Ordner nicht erstellen: {e}")

    def delete_item(self, item_path):
        """Lösche die ausgewählte Datei oder den Ordner."""
        confirm = QMessageBox.question(self, "Löschen bestätigen", f"Sind Sie sicher, dass Sie {item_path} löschen möchten?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    self.parent.output_area.append(f"Datei {item_path} gelöscht.")
                elif os.path.isdir(item_path):
                    os.rmdir(item_path)
                    self.parent.output_area.append(f"Ordner {item_path} gelöscht.")
                self.model.refresh()  # Modell aktualisieren
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Konnte {item_path} nicht löschen: {e}")
