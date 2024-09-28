Das Pluginsystem l�dt automatisch alle Plugins aus dem `plugins`-Ordner, und jedes Plugin wird �ber den `PluginManager` dynamisch initialisiert und ausgef�hrt.

Hier ist eine kurze Zusammenfassung, wie du nun Plugins schreiben kannst, ohne den Hauptcode �ndern zu m�ssen:

### Vorgehensweise f�r das Schreiben neuer Plugins

1. **Erstelle eine neue Datei im `plugins`-Ordner**:
   - Jedes Plugin sollte als eigene Python-Datei im `plugins`-Ordner gespeichert werden.
   - Der Dateiname sollte dem Plugin-Namen entsprechen, z.B. `my_new_plugin.py`.

2. **Implementiere das `PluginInterface`**:
   - Jedes Plugin muss die `initialize`- und `execute`-Methoden des `PluginInterface` implementieren.
   - Die Methode `initialize` wird aufgerufen, wenn das Plugin geladen wird.
   - Die Methode `execute` wird aufgerufen, wenn der Benutzer das Plugin �ber das Men� ausw�hlt.

3. **Beispiel f�r ein neues Plugin (`my_new_plugin.py`)**:

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
        """F�hrt das Plugin aus."""
        self.ide.log_to_output("MyNewPlugin wurde ausgef�hrt.")
        # Hier kannst du deine Plugin-spezifische Logik einf�gen.

# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return MyNewPlugin(ide)
```

4. **Automatisches Laden und Ausf�hren**:
   - Das Plugin wird automatisch geladen und in das Men� eingetragen, wenn du die IDE startest.
   - Der `PluginManager` l�dt alle `.py`-Dateien aus dem `plugins`-Ordner und f�gt sie der IDE hinzu.

5. **Kein Code im Hauptprogramm �ndern**:
   - Du musst **nichts** am Hauptprogramm �ndern. Sobald die neue Plugin-Datei im `plugins`-Ordner liegt und die notwendige Struktur enth�lt, wird es automatisch geladen und ausgef�hrt.

### Erweiterungsm�glichkeiten:

- Du kannst zus�tzliche Plugins schreiben, die komplexere Logik enthalten (z.B. Syntax-Highlighting, Code-Vervollst�ndigung, spezielle Tools, etc.), ohne den Hauptcode zu ber�hren.
- Jedes Plugin kann unabh�ngig arbeiten und eigene Funktionen hinzuf�gen, solange es das `PluginInterface` beachtet.

Mit diesem System kannst du also beliebig viele Plugins erstellen, erweitern oder �ndern, ohne dass der Hauptcode jemals angepasst werden muss.