# cargo_toml_manager.py
import os
import toml

class TomlManager:
    def __init__(self, project_path, output_area):
        self.project_path = project_path
        self.cargo_toml_path = os.path.join(self.project_path, 'Cargo.toml')
        self.output_area = output_area  # Verweis auf das QTextEdit-Ausgabefeld der IDE

    def load_cargo_toml(self):
        """Lade die Cargo.toml Datei und gib ihren Inhalt zurück."""
        if os.path.exists(self.cargo_toml_path):
            try:
                # Versuche, die Datei mit 'utf-8' zu laden
                self.output_area.append("Lade Cargo.toml...")
                with open(self.cargo_toml_path, 'r', encoding='utf-8') as f:
                    self.output_area.append("Cargo.toml Datei erfolgreich geladen.")
                    return toml.load(f)
            except UnicodeDecodeError:
                # Fallback auf 'latin-1', falls 'utf-8' scheitert
                self.output_area.append("Warnung: utf-8 konnte nicht verwendet werden. Fallback auf latin-1.")
                with open(self.cargo_toml_path, 'r', encoding='latin-1') as f:
                    return toml.load(f)
        else:
            self.output_area.append("Cargo.toml Datei nicht gefunden.")
            raise FileNotFoundError("Cargo.toml Datei wurde nicht gefunden.")

    def save_cargo_toml(self, cargo_data):
        """Speichere die geänderte Cargo.toml Datei."""
        self.output_area.append("Speichere Änderungen in der Cargo.toml...")
        with open(self.cargo_toml_path, 'w', encoding='utf-8') as f:
            toml.dump(cargo_data, f)
        self.output_area.append("Änderungen wurden in der Cargo.toml gespeichert.")

    def add_dependency(self, library, version="*"):
        """Füge eine Abhängigkeit zur Cargo.toml hinzu, falls sie noch nicht vorhanden ist."""
        cargo_data = self.load_cargo_toml()

        # Überprüfe, ob [dependencies] Abschnitt existiert, andernfalls erstelle ihn
        if 'dependencies' not in cargo_data:
            cargo_data['dependencies'] = {}

        # Überprüfe, ob die Bibliothek bereits existiert
        if library in cargo_data['dependencies']:
            self.output_area.append(f"Bibliothek {library} ist bereits in der Cargo.toml vorhanden.")
        else:
            # Füge die Bibliothek hinzu und speichere die Datei
            cargo_data['dependencies'][library] = version
            self.save_cargo_toml(cargo_data)
            self.output_area.append(f"Bibliothek {library} wurde hinzugefügt (Version: {version}).")
