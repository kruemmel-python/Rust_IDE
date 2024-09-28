Das Pluginsystem lädt automatisch alle Plugins aus dem `plugins`-Ordner, und jedes Plugin wird über den `PluginManager` dynamisch initialisiert und ausgeführt.

Hier ist eine kurze Zusammenfassung, wie du nun Plugins schreiben kannst, ohne den Hauptcode ändern zu müssen:

### Vorgehensweise für das Schreiben neuer Plugins

1. **Erstelle eine neue Datei im `plugins`-Ordner**:
   - Jedes Plugin sollte als eigene Python-Datei im `plugins`-Ordner gespeichert werden.
   - Der Dateiname sollte dem Plugin-Namen entsprechen, z.B. `my_new_plugin.py`.

2. **Implementiere das `PluginInterface`**:
   - Jedes Plugin muss die `initialize`- und `execute`-Methoden des `PluginInterface` implementieren.
   - Die Methode `initialize` wird aufgerufen, wenn das Plugin geladen wird.
   - Die Methode `execute` wird aufgerufen, wenn der Benutzer das Plugin über das Menü auswählt.

3. **Beispiel für ein neues Plugin (`my_new_plugin.py`)**:

```python
# plugins/my_new_plugin.py
from plugins.plugin_interface import PluginInterface

class MyNewPlugin(PluginInterface):
    def __init__(self, ide):
        self.ide = ide

    def initialize(self):
        """Initialisierung des Plugins."""
        self.ide.log_to_output("MyNewPlugin wurde initialisiert.")

    def execute(self):
        """Führt das Plugin aus."""
        self.ide.log_to_output("MyNewPlugin wurde ausgeführt.")
        # Hier kannst du deine Plugin-spezifische Logik einfügen.

# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return MyNewPlugin(ide)
```

4. **Automatisches Laden und Ausführen**:
   - Das Plugin wird automatisch geladen und in das Menü eingetragen, wenn du die IDE startest.
   - Der `PluginManager` lädt alle `.py`-Dateien aus dem `plugins`-Ordner und fügt sie der IDE hinzu.

5. **Kein Code im Hauptprogramm ändern**:
   - Du musst **nichts** am Hauptprogramm ändern. Sobald die neue Plugin-Datei im `plugins`-Ordner liegt und die notwendige Struktur enthält, wird es automatisch geladen und ausgeführt.

### Erweiterungsmöglichkeiten:

- Du kannst zusätzliche Plugins schreiben, die komplexere Logik enthalten (z.B. Syntax-Highlighting, Code-Vervollständigung, spezielle Tools, etc.), ohne den Hauptcode zu berühren.
- Jedes Plugin kann unabhängig arbeiten und eigene Funktionen hinzufügen, solange es das `PluginInterface` beachtet.

Mit diesem System kannst du also beliebig viele Plugins erstellen, erweitern oder ändern, ohne dass der Hauptcode jemals angepasst werden muss.