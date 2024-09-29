import subprocess
from PyQt5.QtWidgets import QAction, QMessageBox
from plugins.plugin_interface import PluginInterface

class DependencyManagementPlugin(PluginInterface):
    def __init__(self, ide):
        self.ide = ide  # Referenz zur IDE

    def initialize(self):
        """Initialisiert das Plugin und erstellt das Menü für das Dependency Management."""
        # Prüfen, ob das Menü 'Extras' bereits existiert
        extras_menu = None
        for menu in self.ide.menuBar().actions():
            if menu.text() == "Extras":
                extras_menu = menu.menu()
                break

        if not extras_menu:
            extras_menu = self.ide.menuBar().addMenu("Extras")

        # Menüpunkt für die Abhängigkeitsanzeige hinzufügen
        dependencies_action = QAction("Abhängigkeiten anzeigen", self.ide)
        dependencies_action.triggered.connect(self.show_dependencies)
        extras_menu.addAction(dependencies_action)

    def show_dependencies(self):
        """Zeigt die aktuellen Abhängigkeiten des Projekts in sauberem Format an."""
        try:
            # Den Projektpfad dynamisch abrufen
            project_path = self.get_project_path()

            if not project_path:
                self.ide.output_area.append("Fehler: Projektpfad konnte nicht ermittelt werden.")
                return

            # Führe den Befehl `cargo tree` aus, um die Abhängigkeiten zu erhalten
            result = subprocess.run(["cargo", "tree", "--prefix", "none"], capture_output=True, text=True, cwd=project_path)

            if result.returncode != 0:
                self.ide.output_area.append(f"Fehler: {result.stderr}")
                return

            # Verarbeite die Ausgabe, um nur die Bibliotheken und ihre Versionen anzuzeigen
            dependencies = result.stdout.splitlines()
            cleaned_dependencies = []

            for line in dependencies:
                # Filtere Sonderzeichen und nicht relevante Zeilen heraus
                parts = line.split()
                if len(parts) >= 2:
                    # Bibliotheksname und Versionsnummer extrahieren
                    name = parts[0]
                    version = parts[1]
                    cleaned_dependencies.append(f"{name} {version}")

            # Zeige die bereinigten Abhängigkeiten an
            self.ide.output_area.append("Aktuelle Abhängigkeiten:")
            for dep in cleaned_dependencies:
                self.ide.output_area.append(dep)

        except Exception as e:
            self.ide.output_area.append(f"Fehler: {str(e)}")

    def get_project_path(self):
        """Ermittelt den Pfad des aktuellen Projekts."""
        # Beispiel für das Abrufen des Projektpfads, abhängig von der IDE-Implementierung.
        # Hier wird davon ausgegangen, dass die IDE eine Methode `get_project_path` hat, um den Projektpfad abzurufen.
        try:
            project_path = self.ide.rust_integration.current_file
            if project_path:
                # Gehe vom Quellcodeverzeichnis zu dem Projektwurzelverzeichnis
                return project_path.rsplit('/', 2)[0]
            else:
                self.ide.output_area.append("Kein gültiges Projekt geladen.")
                return None
        except AttributeError:
            QMessageBox.warning(self.ide, "Fehler", "Projektpfad konnte nicht ermittelt werden.")
            return None

    def shutdown(self):
        """Aufräumarbeiten beim Schließen des Plugins."""
        pass

# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return DependencyManagementPlugin(ide)
