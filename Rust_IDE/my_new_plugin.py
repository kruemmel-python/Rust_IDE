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
