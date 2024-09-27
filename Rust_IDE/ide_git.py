import os
import subprocess
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QListWidget, QVBoxLayout, QDialog, QPushButton

class GitIntegration:
    def __init__(self, parent):
        self.parent = parent
        # Stelle sicher, dass project_path gesetzt ist
        self.project_path = None  # Zunächst ist kein Projekt geladen

    def set_project_path(self, project_path):
        """Setze den Pfad des aktuell geladenen Projekts."""
        self.project_path = project_path

    def run_git_command(self, command):
        """Führt einen Git-Befehl aus und gibt die Ausgabe zurück."""
        try:
            result = subprocess.run(command, cwd=self.project_path, capture_output=True, text=True, shell=True)
            return result.stdout, result.stderr
        except Exception as e:
            return "", f"Fehler beim Ausführen des Git-Befehls: {str(e)}"

    def commit_changes(self):
        """Erstelle einen Git-Commit."""
        commit_message, ok = QInputDialog.getText(self.parent, "Commit erstellen", "Commit-Nachricht eingeben:")
        if ok and commit_message:
            stdout, stderr = self.run_git_command(f'git add . && git commit -m "{commit_message}"')
            if stderr:
                self.parent.output_area.append(f"Fehler beim Commit: {stderr}")
            else:
                self.parent.output_area.append(f"Commit erfolgreich: {stdout}")

    def push_to_remote(self):
        """Pushe Änderungen zu einem Remote-Repository."""
        stdout, stderr = self.run_git_command('git push')
        if stderr:
            self.parent.output_area.append(f"Fehler beim Push: {stderr}")
        else:
            self.parent.output_area.append(f"Push erfolgreich: {stdout}")

    def pull_from_remote(self):
        """Hole Änderungen von einem Remote-Repository."""
        stdout, stderr = self.run_git_command('git pull')
        if stderr:
            self.parent.output_area.append(f"Fehler beim Pull: {stderr}")
        else:
            self.parent.output_area.append(f"Pull erfolgreich: {stdout}")

    def create_branch(self):
        """Erstelle einen neuen Git-Branch."""
        branch_name, ok = QInputDialog.getText(self.parent, "Neuen Branch erstellen", "Branch-Namen eingeben:")
        if ok and branch_name:
            stdout, stderr = self.run_git_command(f'git branch {branch_name}')
            if stderr:
                self.parent.output_area.append(f"Fehler beim Erstellen des Branches: {stderr}")
            else:
                self.parent.output_area.append(f"Branch {branch_name} erfolgreich erstellt: {stdout}")

    def switch_branch(self):
        """Wechsle zu einem anderen Branch."""
        branch_name, ok = QInputDialog.getText(self.parent, "Branch wechseln", "Branch-Namen eingeben:")
        if ok and branch_name:
            stdout, stderr = self.run_git_command(f'git checkout {branch_name}')
            if stderr:
                self.parent.output_area.append(f"Fehler beim Wechseln des Branches: {stderr}")
            else:
                self.parent.output_area.append(f"Branch gewechselt: {stdout}")

    def view_git_log(self):
        """Zeige den Git-Log an."""
        stdout, stderr = self.run_git_command('git log --oneline')
        if stderr:
            self.parent.output_area.append(f"Fehler beim Anzeigen des Git-Logs: {stderr}")
        else:
            self.parent.output_area.append(f"Git-Log:\n{stdout}")

    def resolve_merge_conflict(self):
        """Zeige Merge-Konflikte an und unterstütze bei der Lösung."""
        stdout, stderr = self.run_git_command('git diff --name-only --diff-filter=U')
        if stderr:
            self.parent.output_area.append(f"Fehler beim Anzeigen der Merge-Konflikte: {stderr}")
        else:
            if stdout.strip():
                self.parent.output_area.append(f"Zu lösende Konflikte:\n{stdout}")
            else:
                self.parent.output_area.append("Keine Konflikte zu lösen.")

    def git_login(self):
        """Git-Anmeldung mit Benutzername und Passwort."""
        username, ok1 = QInputDialog.getText(self.parent, "Git-Anmeldung", "Gib deinen Git-Benutzernamen ein:")
        password, ok2 = QInputDialog.getText(self.parent, "Git-Anmeldung", "Gib dein Git-Passwort ein:")
        if ok1 and ok2 and username and password:
            stdout, stderr = self.run_git_command(f'git config --global user.name "{username}"')
            stdout, stderr = self.run_git_command(f'git config --global user.password "{password}"')
            if stderr:
                self.parent.output_area.append(f"Fehler bei der Git-Anmeldung: {stderr}")
            else:
                self.parent.output_area.append(f"Git-Anmeldung erfolgreich für Benutzer: {username}")
        else:
            self.parent.output_area.append("Git-Anmeldung abgebrochen.")


    def list_repositories(self):
        """Zeige eine Liste der verfügbaren lokalen Git-Repositories an."""
        try:
            # Stelle sicher, dass project_path gültig ist
            if not self.project_path:
                QMessageBox.warning(self.parent, "Fehler", "Kein gültiges Projekt geladen.")
                return

            repos = []
            # Gehe durch alle Verzeichnisse und prüfe, ob sie ein .git-Verzeichnis haben
            for root, dirs, files in os.walk(self.project_path):
                if '.git' in dirs:
                    repos.append(root)

            if repos:
                # Dialog zum Anzeigen der Repositories
                dialog = QDialog(self.parent)
                dialog.setWindowTitle("Verfügbare Git-Repositories")
                layout = QVBoxLayout()

                repo_list = QListWidget()
                for repo in repos:
                    repo_list.addItem(repo)

                # Auswahl-Button für das Laden eines Repositories
                select_button = QPushButton("Repository laden")
                select_button.clicked.connect(lambda: self.load_selected_repository(repo_list.currentItem(), dialog))

                layout.addWidget(repo_list)
                layout.addWidget(select_button)
                dialog.setLayout(layout)
                dialog.exec_()
            else:
                QMessageBox.information(self.parent, "Information", "Keine Git-Repositories gefunden.")
        except Exception as e:
            # Fehlerbehandlung mit QMessageBox anstelle von QErrorMessage
            QMessageBox.critical(self.parent, "Fehler", f"Fehler beim Anzeigen der Repositories: {e}")

    def load_selected_repository(self, selected_repo, dialog):
        """Lade das ausgewählte Repository."""
        if selected_repo is None:
            QMessageBox.warning(self.parent, "Fehler", "Kein Repository ausgewählt.")
            return

        repo_path = selected_repo.text()
        self.parent.rust_integration.project_path = repo_path
        self.parent.output_area.append(f"Repository geladen: {repo_path}")
        dialog.accept()
