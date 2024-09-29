from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit,
    QSplitter, QFileDialog, QMessageBox, QAction, QTabWidget, QMenuBar, QToolBar, QInputDialog
)
from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtGui import QIcon
from editor import RustEditor
from rust_integration import RustIntegration
from explorer import ProjectExplorer
from codestral import CodestralCompletionPlugin
from layout_settings import LayoutSettings
from plugin_manager import PluginManager
from cargo_toml_manager import TomlManager

import subprocess
import os

class RustIDEWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rust IDE mit Plugins")

        # Setze das Fenster-Icon
        icon_path = os.path.join('resources', 'icons', 'project_icon.ico')
        self.setWindowIcon(QIcon(icon_path))

        self.setGeometry(100, 50, 1600, 1000)  # Fenstergröße erweitert

        # Füge das QTabWidget hinzu, das verschiedene Tabs (Editor, Dokumentationsvorschau, Ausgabe) verwaltet
        self.tabs = QTabWidget()

        # Editor mit Syntax-Highlighting
        self.editor = RustEditor()  # Zuerst den Editor initialisieren
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)

        # Füge den Editor-Tab zum Tab-Widget hinzu
        self.tabs.addTab(self.editor, "Editor")

        # Projekt-Explorer initialisieren
        self.project_explorer = ProjectExplorer(self)
        self.project_explorer.setVisible(False)  # Explorer ist standardmäßig ausgeblendet

        # Erster Splitter für Projekt-Explorer (links) und Tabs (rechts)
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.project_explorer)  # Füge den Projekt-Explorer hinzu
        main_splitter.addWidget(self.tabs)  # Füge das Tab-Widget hinzu (nur Editor als Tab)
        main_splitter.setStretchFactor(0, 1)  # Linkes Widget (Explorer) kann schmaler sein
        main_splitter.setStretchFactor(1, 4)  # Rechtes Widget (Tabs) nimmt mehr Platz ein

        # Verwende den Splitter, um den Editor (oben) und die Console (unten) zu trennen
        vertical_splitter = QSplitter(Qt.Vertical)
        vertical_splitter.addWidget(main_splitter)  # Füge den ersten Splitter hinzu (mit Projekt-Explorer und Editor-Tabs)
        vertical_splitter.addWidget(self.output_area)  # Füge die Console als separates Widget hinzu (unterhalb des Editors)
        vertical_splitter.setStretchFactor(0, 4)  # Editor nimmt mehr Platz ein
        vertical_splitter.setStretchFactor(1, 1)  # Console nimmt weniger Platz ein

        # Hauptlayout
        layout = QVBoxLayout()
        layout.addWidget(vertical_splitter)  # Füge den vertikalen Splitter hinzu

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # RustIntegration für Build/Run/Debug
        self.rust_integration = RustIntegration(self)



        # Menüleiste erstellen
        self.create_menu_bar()

        # Layout-Einstellungen initialisieren (nach der Initialisierung des Editors)
        self.layout_settings = LayoutSettings(self)

        # Plugin Manager, übergibt die IDE-Referenz (self)
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_plugins()

        # Menüs erstellen und Plugins einbinden
        menu_bar = self.menuBar()
        plugin_menu = menu_bar.addMenu("Plugins")

        for plugin in self.plugin_manager.plugins:
            action = QAction(plugin.__class__.__name__, self)
            action.triggered.connect(plugin.execute)
            plugin_menu.addAction(action)

        # Hier initialisieren wir das Codestral-Plugin
        self.codestral_plugin = CodestralCompletionPlugin(self)
        # self.codestral_plugin.initialize()



    def create_menu_bar(self):
        from gui.widgets import create_menu_bar as create_menu_bar_func
        create_menu_bar_func(self)

    

    # Weitere API-Interaktionen können hier hinzugefügt werden

    def log_to_output(self, message):
        """Schreibt eine Log-Nachricht in die Ausgabekonsole."""
        self.output_area.append(message)

    def add_action_to_menu(self, menu_name, action):
        """Fügt eine Aktion zu einem vorhandenen Menü hinzu oder erstellt ein neues Menü."""
        menu_bar = self.menuBar()
        menu = menu_bar.findChild(QMenuBar, menu_name)

        if not menu:
            # Falls das Menü noch nicht existiert, erstelle ein neues
            menu = menu_bar.addMenu(menu_name)

        # Füge die Aktion hinzu
        menu.addAction(action)

    def remove_action_from_menu(self, menu_name, action):
        """Entfernt eine Aktion von einem Menü."""
        menu_bar = self.menuBar()
        menu = menu_bar.findChild(QMenuBar, menu_name)

        if menu:
            # Entferne die Aktion, wenn das Menü existiert
            menu.removeAction(action)

    def load_project(self, project_path):
        """Lade das Projekt und zeige den Explorer an."""
        try:
            if not os.path.exists(project_path):
                self.output_area.append(f"Projektpfad existiert nicht: {project_path}")
                QMessageBox.warning(self, "Fehler", "Projektpfad existiert nicht.")
                return

            self.project_explorer.load_project(project_path)
            self.project_explorer.setVisible(True)  # Projekt-Explorer anzeigen

            # Setze den Projektpfad in RustIntegration und lade die Cargo.toml
            self.rust_integration.project_path = project_path
            self.rust_integration.toml_manager = TomlManager(project_path, self.output_area)

            # Git-Integration: Setze den Projektpfad
            self.git_integration.set_project_path(project_path)

            # Überprüfe, ob eine Cargo.toml existiert
            cargo_toml_path = os.path.join(project_path, "Cargo.toml")
            if os.path.exists(cargo_toml_path):
                # Lade die Cargo.toml Datei und zeige sie an
                with open(cargo_toml_path, 'r', encoding='utf-8') as f:
                    cargo_data = f.read()
                    self.editor.setPlainText(cargo_data)
                    self.rust_integration.current_file = cargo_toml_path  # Setze den aktuellen Pfad zur Cargo.toml
                    self.output_area.append(f"Cargo.toml Datei erfolgreich geladen: {cargo_toml_path}")
            else:
                QMessageBox.warning(self, "Fehler", "Cargo.toml Datei nicht gefunden.")
                self.output_area.append("Cargo.toml Datei nicht gefunden.")
                return  # Beende das Laden, wenn keine Cargo.toml vorhanden ist

            # Automatisch die main.rs Datei laden, wenn sie existiert
            main_rs_path = os.path.join(project_path, 'src', 'main.rs')
            if os.path.exists(main_rs_path):
                with open(main_rs_path, 'r', encoding='utf-8') as f:
                    main_rs_data = f.read()
                    self.editor.setPlainText(main_rs_data)
                    self.rust_integration.current_file = main_rs_path  # Setze den aktuellen Pfad zur main.rs
                    self.output_area.append(f"main.rs Datei erfolgreich geladen: {main_rs_path}")
            else:
                QMessageBox.warning(self, "Fehler", "main.rs Datei nicht gefunden.")
                self.output_area.append("main.rs Datei nicht gefunden.")

            self.output_area.append(f"Projekt {project_path} erfolgreich geladen.")
        except Exception as e:
            print(f"Fehler beim Laden des Projekts: {e}")
            QMessageBox.critical(self, "Fehler", f"Fehler beim Laden des Projekts: {e}")

    # Funktion für 'cargo clean'
    def clean_project(self):
        """Funktion zum Bereinigen des Projekts (cargo clean)."""
        if self.rust_integration.project_path:
            # Debugging-Ausgabe
            self.output_area.append(f"Bereinige das Projekt: {self.rust_integration.project_path}")
            process = subprocess.run(["cargo", "clean"], cwd=self.rust_integration.project_path, capture_output=True, text=True)
            self.output_area.setPlainText(process.stdout + process.stderr)
        else:
            self.output_area.setPlainText("Kein Projekt geöffnet.")

    # Funktion für 'gdb target/debug/Projektname'
    def start_gdb(self):
        if self.rust_integration.project_path:
            # Konstruiere den Pfad zur ausführbaren Datei korrekt
            executable_path = os.path.join(self.rust_integration.project_path, 'target', 'debug', 'Rust_Test')

            # Verwende QProcess anstelle von Popen, um gdb nicht zu blockieren
            self.gdb_process = QProcess(self)
            self.gdb_process.setProcessChannelMode(QProcess.MergedChannels)
            self.gdb_process.readyRead.connect(self.read_gdb_output)

            # Starte gdb
            self.gdb_process.start("gdb", [executable_path])

            if not self.gdb_process.waitForStarted():
                self.output_area.setPlainText("Fehler beim Starten von gdb")
        else:
            self.output_area.setPlainText("Kein Projekt geöffnet.")

    def read_gdb_output(self):
        # Lies die Ausgabe des gdb-Prozesses und schreibe sie in die output_area
        output = self.gdb_process.readAllStandardOutput().data().decode()
        self.output_area.append(output)
