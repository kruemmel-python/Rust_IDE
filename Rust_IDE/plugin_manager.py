# plugins/plugin_manager.py
import os
import importlib
from plugins.plugin_interface import PluginInterface

class PluginManager:
    def __init__(self, plugin_directory, ide):
        self.plugin_directory = plugin_directory
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
