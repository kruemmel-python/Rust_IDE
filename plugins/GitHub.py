import requests
from PyQt5.QtWidgets import QMenu, QAction, QInputDialog, QMessageBox
from PyQt5.QtCore import QObject
from plugins.plugin_interface import PluginInterface
import subprocess
import base64
import os

class GitHubPlugin(QObject, PluginInterface):
    def __init__(self, ide):
        super().__init__()
        self.ide = ide
        self.api_token = None
        self.base_url = "https://api.github.com"

    def initialize(self):
        """Initialisiert das Plugin und erstellt das GitHub-Menü."""
        # Erstelle das GitHub-Menü
        github_menu = self.ide.menuBar().addMenu("GitHub")

        # Erstellen der einzelnen Menüpunkte für die verschiedenen GitHub-Funktionen
        self.add_menu_action(github_menu, "Öffentliche Informationen anzeigen", self.show_public_info)
        self.add_menu_action(github_menu, "Vollen Repo-Zugriff anzeigen", self.show_repo_info)
        self.add_menu_action(github_menu, "Commit-Status anzeigen", self.show_commit_status)
        self.add_menu_action(github_menu, "Deployment-Status anzeigen", self.show_repo_deployment)
        self.add_menu_action(github_menu, "Öffentliche Repositories anzeigen", self.show_public_repo)
        self.add_menu_action(github_menu, "Einladungen zu Repositories anzeigen", self.show_repo_invites)
        self.add_menu_action(github_menu, "Security Events anzeigen", self.show_security_events)
        self.add_menu_action(github_menu, "Repository-Hooks verwalten (admin)", self.show_admin_repo_hooks)
        self.add_menu_action(github_menu, "Repository-Hooks verwalten (write)", self.show_write_repo_hooks)
        self.add_menu_action(github_menu, "Repository-Hooks anzeigen (read)", self.show_read_repo_hooks)
        self.add_menu_action(github_menu, "Organisation verwalten (admin)", self.admin_org)
        self.add_menu_action(github_menu, "Organisation verwalten (write)", self.write_org)
        self.add_menu_action(github_menu, "Organisation anzeigen (read)", self.read_org)
        self.add_menu_action(github_menu, "GPG-Schlüssel verwalten (admin)", self.admin_gpg_keys)
        self.add_menu_action(github_menu, "GPG-Schlüssel erstellen (write)", self.write_gpg_keys)
        self.add_menu_action(github_menu, "GPG-Schlüssel anzeigen (read)", self.read_gpg_keys)
        self.add_menu_action(github_menu, "Organisation-Hooks verwalten", self.admin_org_hooks)
        self.add_menu_action(github_menu, "Gists anzeigen", self.show_gists)
        self.add_menu_action(github_menu, "Benachrichtigungen anzeigen", self.show_notifications)
        self.add_menu_action(github_menu, "Benutzerprofil anzeigen", self.show_user_profile)
        self.add_menu_action(github_menu, "E-Mail-Adressen anzeigen", self.show_user_emails)
        self.add_menu_action(github_menu, "Benutzern folgen/entfolgen", self.follow_user)
        self.add_menu_action(github_menu, "Projekte anzeigen (read)", self.read_projects)
        self.add_menu_action(github_menu, "Projekte bearbeiten (write)", self.write_projects)

        # Verwaltung Untermenü für Repository-Operationen
        verwaltung_menu = github_menu.addMenu("Verwaltung")
        self.add_menu_action(verwaltung_menu, "Fork erstellen", self.create_fork)
        self.add_menu_action(verwaltung_menu, "Repository klonen (Herunterladen)", self.clone_repository)
        self.add_menu_action(verwaltung_menu, "Dateien hochladen", self.upload_file_to_repo)
        self.add_menu_action(verwaltung_menu, "Änderungen pushen", self.push_changes)
        self.add_menu_action(verwaltung_menu, "Repo löschen", self.delete_repo)
        self.add_menu_action(verwaltung_menu, "Pakete lesen (read)", self.read_packages)
        self.add_menu_action(verwaltung_menu, "Pakete hochladen (write)", self.write_packages)
        self.add_menu_action(verwaltung_menu, "Pakete löschen", self.delete_packages)
        self.add_menu_action(verwaltung_menu, "Codespaces verwalten", self.manage_codespaces)
        self.add_menu_action(verwaltung_menu, "Workflows verwalten", self.manage_workflows)

        # Token-Aktion zum Setzen des GitHub API-Tokens
        token_action = QAction("API-Token setzen", self.ide)
        token_action.triggered.connect(self.set_api_token)
        github_menu.addAction(token_action)

    def add_menu_action(self, menu, name, callback):
        """Hilfsfunktion zum Hinzufügen von Menüaktionen."""
        action = QAction(name, self.ide)
        action.triggered.connect(callback)
        menu.addAction(action)

    def execute(self):
        """Erforderliche Methode vom PluginInterface."""
        pass

    def set_api_token(self):
        """Fragt den Benutzer nach einem GitHub API-Token."""
        token, ok = QInputDialog.getText(self.ide, "GitHub API Token", "Geben Sie Ihr GitHub API Token ein:")
        if ok and token:
            self.api_token = token
            self.ide.output_area.append("GitHub API Token wurde gesetzt.")

    def make_github_request(self, endpoint, method="GET", data=None):
        """Hilfsfunktion, um eine Anfrage an die GitHub API zu stellen."""
        if not self.api_token:
            QMessageBox.warning(self.ide, "Fehler", "Kein API-Token gesetzt.")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}/{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data)  # PUT wird für Datei-Uploads verwendet
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)

            if response.status_code in range(200, 300):
                return response.json()
            else:
                self.ide.output_area.append(f"Fehler: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.ide.output_area.append(f"Fehler bei der Anfrage: {str(e)}")
            return None

    def get_project_path(self):
        """Gibt den aktuellen Projektpfad aus der IDE zurück."""
        if hasattr(self.ide, 'rust_integration') and self.ide.rust_integration.project_path:
            return self.ide.rust_integration.project_path
        else:
            QMessageBox.warning(self.ide, "Fehler", "Kein Projektpfad gefunden.")
            return None

    def upload_file_to_repo(self):
        """Lädt eine Datei zu einem Repository hoch, mit automatischer Erkennung des Projektpfads und Base64-Kodierung."""
    
        # Automatische Erkennung des Projektpfads
        project_path = self.ide.rust_integration.project_path  # Annahme, dass der Projektpfad hier gespeichert ist
        if not project_path:
            self.ide.output_area.append("Kein Projektpfad gefunden.")
            return

        # Abfrage des Repository-Namens
        repo_name, ok_repo = QInputDialog.getText(self.ide, "Repository", "Geben Sie den Repository-Namen ein (z.B. 'username/repo'):")

        # Automatisch den Dateipfad im Projektordner wählen
        file_path, ok_file = QInputDialog.getText(self.ide, "Dateipfad", f"Geben Sie den Pfad zur Datei im Projekt an ({project_path}):")
        full_file_path = os.path.join(project_path, file_path)

        if ok_repo and ok_file and repo_name and os.path.exists(full_file_path):
            try:
                # Lese den Dateiinhalt und konvertiere ihn in Base64
                with open(full_file_path, "rb") as file:
                    content = base64.b64encode(file.read()).decode("utf-8")  # Base64-kodierter Inhalt
            
                # Erstelle die Nutzdaten für die GitHub API
                data = {
                    "message": "Datei hochgeladen",
                    "content": content  # Base64-kodierter Inhalt
                }
            
                # Sende die Anfrage an die GitHub API
                response = self.make_github_request(f"repos/{repo_name}/contents/{os.path.basename(full_file_path)}", method="PUT", data=data)
            
                if response:
                    self.ide.output_area.append(f"Datei '{full_file_path}' wurde zu Repository '{repo_name}' hochgeladen.")
                else:
                    self.ide.output_area.append(f"Fehler beim Hochladen der Datei '{full_file_path}' zu Repository '{repo_name}'.")
        
            except FileNotFoundError:
                self.ide.output_area.append(f"Datei '{full_file_path}' wurde nicht gefunden.")
        
            except Exception as e:
                self.ide.output_area.append(f"Fehler beim Hochladen der Datei: {str(e)}")
        else:
            self.ide.output_area.append(f"Ungültiger Pfad: '{full_file_path}' oder Repository: '{repo_name}'.")


    def push_changes(self):
        """Pusht Änderungen zu einem Repository (Aktualisieren)."""
        project_path = self.get_project_path()

        if project_path:
            # Frage nach der Commit-Nachricht
            commit_message, ok_msg = QInputDialog.getText(self.ide, "Commit-Nachricht", "Geben Sie eine Commit-Nachricht ein:")
            if not ok_msg or not commit_message:
                self.ide.output_area.append("Keine Commit-Nachricht eingegeben.")
                return

            # Git Add, Commit und Push
            try:
                subprocess.run(["git", "add", "."], cwd=project_path, check=True)
                subprocess.run(["git", "commit", "-m", commit_message], cwd=project_path, check=True)
                result = subprocess.run(["git", "push"], cwd=project_path, capture_output=True, text=True)
                self.ide.output_area.append(result.stdout + result.stderr)
            except subprocess.CalledProcessError as e:
                self.ide.output_area.append(f"Fehler beim Pushen der Änderungen: {str(e)}")
        else:
            self.ide.output_area.append("Fehler: Kein Projektpfad gefunden.")

    # Verwaltungsmethoden
    def create_fork(self):
        """Erstellt einen Fork eines Repositories."""
        repo_name, ok = QInputDialog.getText(self.ide, "Repository forken", "Geben Sie den Repository-Namen ein (z.B. 'username/repo'):")
        if ok and repo_name:
            data = self.make_github_request(f"repos/{repo_name}/forks", method="POST")
            if data:
                self.ide.output_area.append(f"Repository '{repo_name}' wurde erfolgreich geforkt.")

    def clone_repository(self):
        """Klont ein GitHub-Repository (Herunterladen)."""
        repo_url, ok = QInputDialog.getText(self.ide, "Repository klonen", "Geben Sie die URL des Repositorys ein:")
        destination, ok_dest = QInputDialog.getText(self.ide, "Zielverzeichnis", "Geben Sie den Pfad zum Zielverzeichnis ein:")
        if ok and repo_url and ok_dest and destination:
            result = subprocess.run(["git", "clone", repo_url, destination], capture_output=True, text=True)
            self.ide.output_area.append(result.stdout + result.stderr)

    def delete_repo(self):
        """Löscht ein Repository."""
        repo_name, ok = QInputDialog.getText(self.ide, "Repository löschen", "Geben Sie den Repository-Namen ein (z.B. 'username/repo'):")
        if ok and repo_name:
            self.make_github_request(f"repos/{repo_name}", method="DELETE")
            self.ide.output_area.append(f"Repository '{repo_name}' wurde gelöscht.")

    def read_packages(self):
        """Zeigt Pakete an."""
        self.ide.output_area.append("Pakete (read) werden angezeigt...")

    def write_packages(self):
        """Hochladen von Paketen."""
        self.ide.output_area.append("Pakete (write) werden hochgeladen...")

    def delete_packages(self):
        """Löschen von Paketen."""
        self.ide.output_area.append("Pakete werden gelöscht...")

    def manage_codespaces(self):
        """Verwalten von Codespaces."""
        self.ide.output_area.append("Codespaces werden verwaltet...")

    def manage_workflows(self):
        """Verwalten von Workflows."""
        self.ide.output_area.append("Workflows werden verwaltet...")

    def show_public_info(self):
        """Zeigt öffentliche Informationen an."""
        data = self.make_github_request("user")
        if data:
            self.ide.output_area.append(f"Öffentliche Benutzerinformationen: {data}")

    def show_repo_info(self):
        """Zeigt Informationen zu Repositories an."""
        repo_name, ok = QInputDialog.getText(self.ide, "Repository", "Geben Sie den Repository-Namen ein (z.B. 'username/repo'):")
        if ok and repo_name:
            data = self.make_github_request(f"repos/{repo_name}")
            if data:
                self.ide.output_area.append(f"Repository-Informationen: {data}")

    def show_commit_status(self):
        """Zeigt den Commit-Status eines Repositories an."""
        repo_name, ok = QInputDialog.getText(self.ide, "Repository", "Geben Sie den Repository-Namen ein (z.B. 'username/repo'):")
        if ok and repo_name:
            data = self.make_github_request(f"repos/{repo_name}/commits")
            if data:
                self.ide.output_area.append(f"Commit-Status für Repository '{repo_name}': {data}")

    def show_repo_deployment(self):
        """Zeigt den Deployment-Status eines Repositories an."""
        repo_name, ok = QInputDialog.getText(self.ide, "Repository", "Geben Sie den Repository-Namen ein (z.B. 'username/repo'):")
        if ok and repo_name:
            data = self.make_github_request(f"repos/{repo_name}/deployments")
            if data:
                self.ide.output_area.append(f"Deployment-Status für Repository '{repo_name}': {data}")

    def show_public_repo(self):
        """Zeigt öffentliche Repositories an."""
        data = self.make_github_request("repositories")
        if data:
            self.ide.output_area.append(f"Öffentliche Repositories: {data}")

    def show_repo_invites(self):
        """Zeigt Repository-Einladungen an."""
        data = self.make_github_request("user/repository_invitations")
        if data:
            self.ide.output_area.append(f"Repository-Einladungen: {data}")

    def show_security_events(self):
        """Zeigt Security Events eines Repositories an."""
        repo_name, ok = QInputDialog.getText(self.ide, "Repository", "Geben Sie den Repository-Namen ein (z.B. 'username/repo'):")
        if ok and repo_name:
            data = self.make_github_request(f"repos/{repo_name}/code-scanning/alerts")
            if data:
                self.ide.output_area.append(f"Security Events für Repository '{repo_name}': {data}")

    def show_admin_repo_hooks(self):
        """Zeigt Admin-Zugriff auf Repository-Hooks an."""
        repo_name, ok = QInputDialog.getText(self.ide, "Repository", "Geben Sie den Repository-Namen ein (z.B. 'username/repo'):")
        if ok and repo_name:
            data = self.make_github_request(f"repos/{repo_name}/hooks")
            if data:
                self.ide.output_area.append(f"Repository-Hooks für '{repo_name}': {data}")

    def show_write_repo_hooks(self):
        """Verwaltet Repository-Hooks mit Schreibzugriff."""
        repo_name, ok = QInputDialog.getText(self.ide, "Repository", "Geben Sie den Repository-Namen ein (z.B. 'username/repo'):")
        if ok and repo_name:
            data = self.make_github_request(f"repos/{repo_name}/hooks")
            if data:
                self.ide.output_area.append(f"Schreibzugriff auf Repository-Hooks für '{repo_name}': {data}")

    def show_read_repo_hooks(self):
        """Zeigt Lesezugriff auf Repository-Hooks an."""
        repo_name, ok = QInputDialog.getText(self.ide, "Repository", "Geben Sie den Repository-Namen ein (z.B. 'username/repo'):")
        if ok and repo_name:
            data = self.make_github_request(f"repos/{repo_name}/hooks")
            if data:
                self.ide.output_area.append(f"Lesezugriff auf Repository-Hooks für '{repo_name}': {data}")

    def admin_org(self):
        """Verwaltet die Organisation mit Admin-Rechten."""
        org_name, ok = QInputDialog.getText(self.ide, "Organisation", "Geben Sie den Namen der Organisation ein:")
        if ok and org_name:
            data = self.make_github_request(f"orgs/{org_name}")
            if data:
                self.ide.output_area.append(f"Organisation '{org_name}' verwaltet: {data}")

    def write_org(self):
        """Verwaltet Schreibzugriff auf Organisationen."""
        org_name, ok = QInputDialog.getText(self.ide, "Organisation verwalten (write)", "Geben Sie den Namen der Organisation ein:")
        if ok and org_name:
            data = self.make_github_request(f"orgs/{org_name}", method="PATCH")  # Verwende PATCH, um Organisationsdaten zu ändern
            if data:
                self.ide.output_area.append(f"Schreibzugriff auf Organisation '{org_name}' erfolgreich verwaltet: {data}")
            else:
                self.ide.output_area.append(f"Fehler beim Verwalten der Organisation '{org_name}'.")

    def read_org(self):
        """Zeigt Informationen über eine Organisation an."""
        org_name, ok = QInputDialog.getText(self.ide, "Organisation anzeigen (read)", "Geben Sie den Namen der Organisation ein:")
        if ok and org_name:
            data = self.make_github_request(f"orgs/{org_name}")
            if data:
                self.ide.output_area.append(f"Organisation '{org_name}' Informationen: {data}")
            else:
                self.ide.output_area.append(f"Fehler beim Abrufen der Organisation '{org_name}'.")

    def admin_gpg_keys(self):
        """Verwaltet GPG-Schlüssel mit Admin-Rechten."""
        data = self.make_github_request("user/gpg_keys")
        if data:
            self.ide.output_area.append(f"Admin GPG-Schlüssel: {data}")

    def write_gpg_keys(self):
        """Erstellt oder verwaltet GPG-Schlüssel."""
        key, ok = QInputDialog.getText(self.ide, "GPG-Schlüssel hinzufügen", "Geben Sie den GPG-Schlüssel ein:")
        if ok and key:
            data = {
                "armored_public_key": key
            }
            self.make_github_request("user/gpg_keys", method="POST", data=data)
            self.ide.output_area.append("GPG-Schlüssel erfolgreich hinzugefügt.")

    def read_gpg_keys(self):
        """Zeigt GPG-Schlüssel an."""
        data = self.make_github_request("user/gpg_keys")
        if data:
            self.ide.output_area.append(f"GPG-Schlüssel: {data}")

    def admin_org_hooks(self):
        """Verwaltet Organisations-Hooks."""
        org_name, ok = QInputDialog.getText(self.ide, "Organisation", "Geben Sie den Namen der Organisation ein:")
        if ok and org_name:
            data = self.make_github_request(f"orgs/{org_name}/hooks")
            if data:
                self.ide.output_area.append(f"Organisation-Hooks für '{org_name}': {data}")

    def show_gists(self):
        """Zeigt die Gists des Benutzers an."""
        data = self.make_github_request("gists")
        if data:
            self.ide.output_area.append(f"Gists: {data}")

    def show_notifications(self):
        """Zeigt Benachrichtigungen des Benutzers an."""
        data = self.make_github_request("notifications")
        if data:
            self.ide.output_area.append(f"Benachrichtigungen: {data}")

    def show_user_profile(self):
        """Zeigt das Benutzerprofil an."""
        data = self.make_github_request("user")
        if data:
            self.ide.output_area.append(f"Benutzerprofil: {data}")

    def show_user_emails(self):
        """Zeigt die E-Mail-Adressen des Benutzers an."""
        data = self.make_github_request("user/emails")
        if data:
            self.ide.output_area.append(f"E-Mail-Adressen: {data}")

    def follow_user(self):
        """Folgt oder entfolgt einem Benutzer."""
        username, ok = QInputDialog.getText(self.ide, "Benutzer", "Geben Sie den Benutzernamen ein, dem Sie folgen möchten:")
        if ok and username:
            data = self.make_github_request(f"user/following/{username}", method="PUT")
            if data:
                self.ide.output_area.append(f"Sie folgen jetzt '{username}'.")

    def read_projects(self):
        """Zeigt Projekte mit Leserechten an."""
        data = self.make_github_request("user/projects")
        if data:
            self.ide.output_area.append(f"Projekte (read): {data}")

    def write_projects(self):
        """Verwaltet Projekte mit Schreibrechten."""
        project_name, ok = QInputDialog.getText(self.ide, "Projekt erstellen", "Geben Sie den Projektnamen ein:")
        if ok and project_name:
            data = {
                "name": project_name
            }
            self.make_github_request("user/projects", method="POST", data=data)
            self.ide.output_area.append(f"Projekt '{project_name}' erstellt.")


# Factory-Funktion, um das Plugin zu erstellen
def create_plugin(ide):
    return GitHubPlugin(ide)
