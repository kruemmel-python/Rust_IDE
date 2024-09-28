import os
import subprocess
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QDialog, QVBoxLayout, QListWidget, QPushButton


class GitIntegration:
    def __init__(self, parent):
        self.parent = parent
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

    def add_remote_repository(self, remote_url):
        """Fügt ein Remote-Repository hinzu."""
        stdout, stderr = self.run_git_command(f'git remote add origin {remote_url}')
        if stderr:
            self.parent.output_area.append(f"Fehler beim Hinzufügen des Remote-Repositorys: {stderr}")
        else:
            self.parent.output_area.append(f"Remote-Repository erfolgreich hinzugefügt: {stdout}")

    def check_and_push_to_github(self):
        """Überprüft, ob ein Remote existiert und pusht das Projekt zu GitHub."""
        stdout, stderr = self.run_git_command('git remote -v')
        if "origin" not in stdout:
            # Falls kein Remote vorhanden ist, fordere den Benutzer auf, die GitHub-URL einzugeben
            remote_url, ok = QInputDialog.getText(self.parent, "Remote-Repository hinzufügen", "Gib die GitHub-URL ein:")
            if ok and remote_url:
                self.add_remote_repository(remote_url)
                self.push_to_github()
            else:
                self.parent.output_area.append("Push abgebrochen. Keine GitHub-URL angegeben.")
        else:
            # Falls ein Remote bereits existiert, einfach pushen
            self.push_to_github()

    def push_to_github(self):
        """Pushe das Projekt auf das Remote-Repository (GitHub)."""
        stdout, stderr = self.run_git_command('git push --set-upstream origin master')
        if stderr:
            self.parent.output_area.append(f"Fehler beim Push: {stderr}")
        else:
            self.parent.output_area.append(f"Projekt erfolgreich auf GitHub hochgeladen: {stdout}")

    def pull_from_remote(self):
        """Hole Änderungen von einem Remote-Repository."""
        remote, ok = QInputDialog.getText(self.parent, "Pull ausführen", "Remote-Namen und Branch eingeben (z.B. 'origin master'):")
        if ok and remote:
            stdout, stderr = self.run_git_command(f'git pull {remote}')
            if stderr:
                self.parent.output_area.append(f"Fehler beim Pull: {stderr}")
            else:
                self.parent.output_area.append(f"Pull erfolgreich: {stdout}")

    def create_branch(self):
        """Erstelle einen neuen Git-Branch."""
        branch_name, ok = QInputDialog.getText(self.parent, "Neuen Branch erstellen", "Branch-Namen eingeben:")
        if ok and branch_name:
            branch_name = branch_name.strip()
            stdout, stderr = self.run_git_command(f'git branch {branch_name}')
            if stderr:
                self.parent.output_area.append(f"Fehler beim Erstellen des Branches: {stderr}")
            else:
                self.parent.output_area.append(f"Branch {branch_name} erfolgreich erstellt.")

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
        """Methode zur Git-Anmeldung (Dummy-Implementierung)."""
        self.parent.output_area.append("Git-Anmeldung erfolgreich.")

    def list_repositories(self):
        """Methode zum Anzeigen der Repositories (Dummy-Implementierung)."""
        self.parent.output_area.append("Repositories angezeigt.")


