# widgets.py
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtGui import QKeySequence
from ide_git import GitIntegration  # Neue Git-Integration
from codestral import CodestralCompletionPlugin 
from layout import LayoutSettings  # Importiere die LayoutSettings

def create_menu_bar(parent):
    menubar = parent.menuBar()

    # "Datei"-Menü
    file_menu = menubar.addMenu('Datei')

    # Einstellungs-Menü für Layout
    settings_menu = menubar.addMenu('Einstellungen')

    change_font_action = QAction('Schriftart ändern', parent)
    change_font_action.triggered.connect(lambda: parent.layout_settings.change_font())
    settings_menu.addAction(change_font_action)

    change_font_size_action = QAction('Schriftgröße ändern', parent)
    change_font_size_action.triggered.connect(lambda: parent.layout_settings.change_font_size())
    settings_menu.addAction(change_font_size_action)
   
    new_project_action = QAction('Neues Projekt', parent)
    new_project_action.triggered.connect(parent.rust_integration.new_project)
    file_menu.addAction(new_project_action)

    open_project_action = QAction('Projekt öffnen', parent)
    open_project_action.triggered.connect(lambda: open_project(parent))  # Verwende die Methode aus window.py
    file_menu.addAction(open_project_action)

    open_cargo_action = QAction('Cargo.toml öffnen', parent)
    open_cargo_action.triggered.connect(parent.rust_integration.open_cargo_toml)
    file_menu.addAction(open_cargo_action)

    save_project_action = QAction('Projekt speichern', parent)
    save_project_action.triggered.connect(parent.rust_integration.save_project)
    file_menu.addAction(save_project_action)

    # Build-Menü
    build_menu = menubar.addMenu('Build')

    build_action = QAction('Build & Run', parent)
    build_action.setShortcut(QKeySequence("Ctrl+B"))  # Tastenkürzel
    build_action.triggered.connect(parent.rust_integration.run_rust_code)
    build_menu.addAction(build_action)

    clean_action = QAction('Clean Project', parent)
    clean_action.setShortcut(QKeySequence("Ctrl+Shift+C"))  # Tastenkürzel
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
    start_debugger_action.setShortcut(QKeySequence("Ctrl+D"))  # Tastenkürzel
    start_debugger_action.triggered.connect(parent.rust_integration.start_debugger)
    debug_menu.addAction(start_debugger_action)

    run_debugger_action = QAction('Run Debugger', parent)
    run_debugger_action.setShortcut(QKeySequence("Ctrl+R"))  # Tastenkürzel
    run_debugger_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('run'))
    debug_menu.addAction(run_debugger_action)

    breakpoint_action = QAction('Set Breakpoint (main)', parent)
    breakpoint_action.setShortcut(QKeySequence("Ctrl+Shift+B"))  # Tastenkürzel
    breakpoint_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('break main'))
    debug_menu.addAction(breakpoint_action)

    step_action = QAction('Step (F10)', parent)
    step_action.setShortcut(QKeySequence("F10"))  # Tastenkürzel
    step_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('step'))
    debug_menu.addAction(step_action)

    next_action = QAction('Next (F11)', parent)
    next_action.setShortcut(QKeySequence("F11"))  # Tastenkürzel
    next_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('next'))
    debug_menu.addAction(next_action)

    continue_action = QAction('Continue (F5)', parent)
    continue_action.setShortcut(QKeySequence("F5"))  # Tastenkürzel
    continue_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('continue'))
    debug_menu.addAction(continue_action)

    quit_action = QAction('Quit Debugger', parent)
    quit_action.setShortcut(QKeySequence("Ctrl+Q"))  # Tastenkürzel
    quit_action.triggered.connect(lambda: parent.rust_integration.send_gdb_command('quit'))
    debug_menu.addAction(quit_action)

    # Git-Menü
    # Git-Menü
    git_menu = menubar.addMenu('Git')

    git_integration = parent.git_integration

    commit_action = QAction('Commit erstellen', parent)
    commit_action.triggered.connect(lambda: git_integration.commit_changes())
    git_menu.addAction(commit_action)

    push_action = QAction('Push', parent)
    push_action.triggered.connect(lambda: git_integration.push_to_remote())
    git_menu.addAction(push_action)

    pull_action = QAction('Pull', parent)
    pull_action.triggered.connect(lambda: git_integration.pull_from_remote())
    git_menu.addAction(pull_action)

    branch_create_action = QAction('Neuen Branch erstellen', parent)
    branch_create_action.triggered.connect(lambda: git_integration.create_branch())
    git_menu.addAction(branch_create_action)

    branch_switch_action = QAction('Branch wechseln', parent)
    branch_switch_action.triggered.connect(lambda: git_integration.switch_branch())
    git_menu.addAction(branch_switch_action)

    log_action = QAction('Git-Log anzeigen', parent)
    log_action.triggered.connect(lambda: git_integration.view_git_log())
    git_menu.addAction(log_action)

    resolve_conflict_action = QAction('Merge-Konflikte lösen', parent)
    resolve_conflict_action.triggered.connect(lambda: git_integration.resolve_merge_conflict())
    git_menu.addAction(resolve_conflict_action)

    login_action = QAction('Git-Anmeldung', parent)
    login_action.triggered.connect(lambda: git_integration.git_login())
    git_menu.addAction(login_action)

    list_repos_action = QAction('Repositories anzeigen', parent)
    list_repos_action.triggered.connect(lambda: git_integration.list_repositories())
    git_menu.addAction(list_repos_action)

    # Codestral Code Vervollständigung ins Menü einfügen
    complete_code_action = QAction("Code vervollständigen", parent)
    complete_code_action.triggered.connect(lambda: parent.codestral_plugin.complete_code())
    menubar.addAction(complete_code_action)  # Hinzufügen zur Menüleiste unter dem Hauptmenü

def open_project(parent):
    """Dialog für das Öffnen eines Projekts"""
    project_path = QFileDialog.getExistingDirectory(parent, "Projektordner auswählen", "")
    if project_path:
        parent.load_project(project_path)
