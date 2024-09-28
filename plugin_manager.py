import os
import importlib
import sys
from plugins.plugin_interface import PluginInterface

class PluginManager:
    def __init__(self, ide):
        # Bestimme den aktuellen Verzeichnis-Pfad
        if getattr(sys, 'frozen', False):
            # Wenn das Skript in einer EXE läuft
            self.plugin_directory = os.path.join(sys._MEIPASS, 'plugins')
        else:
            # Wenn das Skript in der Entwicklungsumgebung läuft
            self.plugin_directory = os.path.join(os.path.dirname(__file__), 'plugins')

        self.plugins = []
        self.ide = ide  # Speichert die IDE-Referenz

    def load_plugins(self):
        """Lädt alle Plugins aus dem Verzeichnis"""
        for filename in os.listdir(self.plugin_directory):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                module = importlib.import_module(f"plugins.{module_name}")
                for attr in dir(module):
                    plugin_class = getattr(module, attr)
                    if isinstance(plugin_class, type) and issubclass(plugin_class, PluginInterface) and plugin_class is not PluginInterface:
                        # Übergibt die IDE-Referenz beim Instanziieren des Plugins
                        plugin_instance = plugin_class(self.ide)
                        plugin_instance.initialize()
                        self.plugins.append(plugin_instance)
