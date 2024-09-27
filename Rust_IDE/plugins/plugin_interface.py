# plugins/plugin_interface.py
class PluginInterface:
    def initialize(self):
        """Initialisiert das Plugin"""
        raise NotImplementedError("Plugins müssen die initialize-Methode implementieren")

    def execute(self):
        """Führt das Plugin aus"""
        raise NotImplementedError("Plugins müssen die execute-Methode implementieren")
