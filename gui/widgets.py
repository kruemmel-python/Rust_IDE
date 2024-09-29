from PyQt5.QtWidgets import QAction, QFileDialog, QMessageBox, QMenu, QMenuBar
from PyQt5.QtGui import QKeySequence


def create_menu_bar(parent):
    """Erstellt die Menüleiste für die Rust IDE mit allen relevanten Menüs und Aktionen."""

    menubar = parent.menuBar()

    # "Datei"-Menü
    file_menu = menubar.addMenu('Datei')

    # Aktion: Projekt öffnen
    open_project_action = QAction('Projekt öffnen', parent)
    open_project_action.triggered.connect(lambda: open_project(parent))
    file_menu.addAction(open_project_action)

    # Aktion: Neues Projekt erstellen
    new_project_action = QAction('Neues Projekt erstellen', parent)
    new_project_action.triggered.connect(lambda: parent.rust_integration.new_project())  # Verknüpfe die Aktion mit new_project
    file_menu.addAction(new_project_action)

    # Aktion: Cargo.toml öffnen
    open_cargo_action = QAction('Cargo.toml öffnen', parent)
    open_cargo_action.triggered.connect(parent.rust_integration.open_cargo_toml)
    file_menu.addAction(open_cargo_action)

    # Aktion: Projekt speichern
    save_project_action = QAction('Projekt speichern', parent)
    save_project_action.triggered.connect(parent.rust_integration.save_project)
    file_menu.addAction(save_project_action)

    # Einstellungs-Menü für Layout
    settings_menu = menubar.addMenu('Einstellungen')

    # Schriftart ändern
    change_font_action = QAction('Schriftart ändern', parent)
    change_font_action.triggered.connect(lambda: parent.layout_settings.change_font())
    settings_menu.addAction(change_font_action)

    # Schriftgröße ändern
    change_font_size_action = QAction('Schriftgröße ändern', parent)
    change_font_size_action.triggered.connect(lambda: parent.layout_settings.change_font_size())
    settings_menu.addAction(change_font_size_action)

    # Hintergrundfarbe des Editors ändern
    change_editor_bg_action = QAction('Hintergrundfarbe des Editors ändern', parent)
    change_editor_bg_action.triggered.connect(lambda: parent.layout_settings.change_editor_bg_color())
    settings_menu.addAction(change_editor_bg_action)

    # Hintergrundfarbe der Ausgabe ändern
    change_output_bg_action = QAction('Hintergrundfarbe der Ausgabe ändern', parent)
    change_output_bg_action.triggered.connect(lambda: parent.layout_settings.change_output_bg_color())
    settings_menu.addAction(change_output_bg_action)

    # Hintergrundfarbe des Projekt-Explorers ändern
    change_explorer_bg_action = QAction('Hintergrundfarbe des Projekt-Explorers ändern', parent)
    change_explorer_bg_action.triggered.connect(lambda: parent.layout_settings.change_explorer_bg_color())
    settings_menu.addAction(change_explorer_bg_action)

    # Hintergrundfarbe des Fensters ändern
    change_window_bg_action = QAction('Hintergrundfarbe des Fensters ändern', parent)
    change_window_bg_action.triggered.connect(lambda: parent.layout_settings.change_window_bg_color())
    settings_menu.addAction(change_window_bg_action)

    # Textfarbe des Editors ändern
    change_editor_text_action = QAction('Textfarbe des Editors ändern', parent)
    change_editor_text_action.triggered.connect(lambda: parent.layout_settings.change_editor_text_color())
    settings_menu.addAction(change_editor_text_action)

    # Textfarbe der Ausgabe ändern
    change_output_text_action = QAction('Textfarbe der Ausgabe ändern', parent)
    change_output_text_action.triggered.connect(lambda: parent.layout_settings.change_output_text_color())
    settings_menu.addAction(change_output_text_action)

    # Textfarbe des Projekt-Explorers ändern
    change_explorer_text_action = QAction('Textfarbe des Projekt-Explorers ändern', parent)
    change_explorer_text_action.triggered.connect(lambda: parent.layout_settings.change_explorer_text_color())
    settings_menu.addAction(change_explorer_text_action)

    # Textfarbe der Menüleiste ändern
    change_menu_text_action = QAction('Textfarbe der Menüleiste ändern', parent)
    change_menu_text_action.triggered.connect(lambda: parent.layout_settings.change_menu_text_color())
    settings_menu.addAction(change_menu_text_action)

    # Zurücksetzen auf Standard
    reset_defaults_action = QAction('Layout zurücksetzen', parent)
    reset_defaults_action.triggered.connect(lambda: parent.layout_settings.reset_to_default())
    settings_menu.addAction(reset_defaults_action)

    # Build-Menü
    build_menu = menubar.addMenu('Build')

    build_action = QAction('Build & Run', parent)
    build_action.setShortcut(QKeySequence("Ctrl+B"))
    build_action.triggered.connect(parent.rust_integration.run_rust_code)
    build_menu.addAction(build_action)

    clean_action = QAction('Clean Project', parent)
    clean_action.setShortcut(QKeySequence("Ctrl+Shift+C"))
    clean_action.triggered.connect(parent.clean_project)
    build_menu.addAction(clean_action)

    # Build-Modus-Menü
    build_mode_menu = menubar.addMenu('Build-Modus')

    debug_action = QAction('Debug', parent, checkable=True)
    debug_action.setChecked(True)
    debug_action.triggered.connect(parent.rust_integration.set_debug_mode)
    build_mode_menu.addAction(debug_action)

    release_action = QAction('Release', parent, checkable=True)
    release_action.triggered.connect(parent.rust_integration.set_release_mode)
    build_mode_menu.addAction(release_action)

    # Debugger-Menü
    debug_menu = menubar.addMenu('Debugger')

    start_debugger_action = QAction('Start Debugger', parent)
    start_debugger_action.setShortcut(QKeySequence("Ctrl+D"))
    start_debugger_action.triggered.connect(parent.rust_integration.start_debugger)
    debug_menu.addAction(start_debugger_action)

    run_debugger_action = QAction('Run Debugger', parent)
    run_debugger_action.setShortcut(QKeySequence("Ctrl+R"))
    run_debugger_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('run'))
    debug_menu.addAction(run_debugger_action)

    breakpoint_action = QAction('Set Breakpoint (main)', parent)
    breakpoint_action.setShortcut(QKeySequence("Ctrl+Shift+B"))
    breakpoint_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('break main'))
    debug_menu.addAction(breakpoint_action)

    step_action = QAction('Step (F10)', parent)
    step_action.setShortcut(QKeySequence("F10"))
    step_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('step'))
    debug_menu.addAction(step_action)

    next_action = QAction('Next (F11)', parent)
    next_action.setShortcut(QKeySequence("F11"))
    next_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('next'))
    debug_menu.addAction(next_action)

    continue_action = QAction('Continue (F5)', parent)
    continue_action.setShortcut(QKeySequence("F5"))
    continue_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('continue'))
    debug_menu.addAction(continue_action)

    quit_action = QAction('Quit Debugger', parent)
    quit_action.setShortcut(QKeySequence("Ctrl+Q"))
    quit_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('quit'))
    debug_menu.addAction(quit_action)

    
    # Codestral Code-Vervollständigung ins Menü einfügen
    complete_code_action = QAction("Code vervollständigen", parent)
    complete_code_action.triggered.connect(lambda: parent.codestral_plugin.complete_code())
    menubar.addAction(complete_code_action)  # Hinzufügen zur Menüleiste unter dem Hauptmenü

def open_project(parent):
    """Dialog für das Öffnen eines Projekts."""
    project_path = QFileDialog.getExistingDirectory(parent, "Projektordner auswählen", "")
    if project_path:
        parent.load_project(project_path)
