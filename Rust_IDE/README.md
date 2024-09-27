
---

# Rust IDE

Eine umfassende Entwicklungsumgebung für Rust, die alle wesentlichen Funktionen zur Entwicklung, Erstellung und zum Debuggen von Rust-Projekten bietet. Die IDE unterstützt das Erstellen neuer Rust-Projekte, das Öffnen bestehender Projekte, die Verwaltung von Abhängigkeiten über die `Cargo.toml` und bietet einen integrierten Debugger. Zusätzlich gibt es erweiterte Funktionen wie **Git-Integration**, **KI-Codevervollständigung** und **Layout-Anpassungen**.

## Installation

### Rust installieren

Um die Rust-Entwicklungsumgebung auf deinem System zu installieren, führe den folgenden Befehl im Terminal oder der Eingabeaufforderung aus:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Dieser Befehl installiert Rust, `cargo` (das Build-System und Paketmanagement-Tool von Rust) sowie das Tool `rustup` zur Verwaltung von Toolchains.

### Installation der Windows-Toolchain

Falls du auf Windows arbeitest, wirst du auch die **Visual Studio Build Tools** benötigen, um Rust mit der MSVC-Toolchain zu verwenden.

1. Lade die **Visual Studio Build Tools** herunter und installiere sie von der folgenden Webseite:
   [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

2. Wähle während der Installation die Option "Desktop development with C++" aus.

3. Nach der Installation kannst du sicherstellen, dass Rust die richtige Toolchain verwendet, indem du den folgenden Befehl ausführst:

```bash
rustup default stable-x86_64-pc-windows-msvc
```

### Python und Abhängigkeiten

Zusätzlich zu Rust benötigst du Python und einige Python-Bibliotheken, um die IDE auszuführen:

```bash
pip install PyQt5 toml requests pyperclip
```

## Anwendungshinweise

- **Projekt erstellen**: Wähle `Datei -> Neues Projekt`, um ein neues Rust-Projekt zu erstellen.
- **Projekt öffnen**: Öffne ein bestehendes Rust-Projekt über `Datei -> Projekt öffnen`.
- **Build & Run**: Verwende `Ctrl+B`, um das aktuelle Projekt zu kompilieren und auszuführen.
- **Debugger**: Nutze die integrierten Debugger-Funktionen, um Haltepunkte zu setzen und den Programmablauf zu steuern.
- **Code vervollständigen**: Über `Code -> Code vervollständigen` kannst du die KI nutzen, um den aktuellen Code automatisch vervollständigen zu lassen.
- **Layout ändern**: Passe über `Einstellungen -> Layout` die Schriftgröße und den Schriftstil im Editor an.
- **Git-Integration**: Erstelle Commits, push/pull zu einem Remote-Repository oder wechsle Branches direkt über das `Git`-Menü.

## Funktionen

### 1. Projektverwaltung

- **Neues Projekt erstellen**: Über das Menü `Datei -> Neues Projekt` kann ein neues Rust-Projekt erstellt werden. Die `Cargo.toml` wird automatisch erstellt und konfiguriert.
- **Projekt öffnen**: Bestehende Projekte können über `Datei -> Projekt öffnen` geladen werden. Der Projektbaum wird im Explorer angezeigt, und Dateien können durch Doppelklick im Editor bearbeitet werden.
- **Cargo.toml öffnen**: Die `Cargo.toml`-Datei des Projekts kann über `Datei -> Cargo.toml öffnen` bearbeitet werden. Abhängigkeiten werden automatisch hinzugefügt, basierend auf dem Code im Projekt.
- **Projekt speichern**: Speichert die aktuell im Editor geöffnete Datei über `Datei -> Projekt speichern`. Abhängigkeiten werden automatisch erkannt und in der `Cargo.toml`-Datei aktualisiert.

### 2. Editor

- **Syntax-Highlighting**: Der integrierte Editor unterstützt Rust-Syntax-Highlighting für Schlüsselwörter, Kommentare und Strings.
- **Code-Vervollständigung mit KI**: Der Editor ist mit einer **KI-basierten Codevervollständigung** (via Codestral) ausgestattet. Der Code kann automatisch ergänzt werden, indem du im Menü `Code -> Code vervollständigen` auswählst.

### 3. Build- und Run-Funktionen

- **Build & Run**: Über das Menü `Build -> Build & Run` oder den Shortcut `Ctrl + B` kann das Projekt kompiliert und ausgeführt werden. Der Fortschritt und die Ausgabe werden im unteren Ausgabefenster der IDE angezeigt.
- **Clean Project**: Bereinigt das Projektverzeichnis von Build-Artefakten über `Build -> Clean Project` oder den Shortcut `Ctrl + Shift + C`.

### 4. Build-Modus wechseln

- Wechsle zwischen Debug- und Release-Modus im Menü `Build-Modus`. Der Debug-Modus erstellt das Projekt mit zusätzlichen Debugging-Informationen, während der Release-Modus für optimale Leistung optimiert ist.

### 5. Debugger

Das Debugging-Menü ist vollständig in die IDE integriert. Es verwendet GDB zur Untersuchung des Programmablaufs, setzt Haltepunkte und bietet die Möglichkeit, den Code schrittweise zu durchlaufen.

- **Start Debugger (`Ctrl+D`)**: Startet den Debugger im Debug-Modus.
- **Run Debugger (`Ctrl+R`)**: Startet das Programm im Debugger.
- **Set Breakpoint (main) (`Ctrl+Shift+B`)**: Setzt einen Haltepunkt in der `main`-Funktion.
- **Step (`F10`)**: Führt einen Einzelschritt im Debugger aus.
- **Next (`F11`)**: Springt zum nächsten Schritt im Code.
- **Continue (`F5`)**: Setzt die Ausführung im Debugger fort.
- **Quit Debugger (`Ctrl+Q`)**: Beendet die Debugger-Sitzung.

### 6. Layout-Anpassungen

Über das Menü `Einstellungen -> Layout` kannst du die Schriftart und -größe im Editor anpassen. Diese Funktion bietet Flexibilität bei der Gestaltung der Arbeitsumgebung und verbessert die Lesbarkeit.

### 7. Projekt-Abhängigkeiten

- Die IDE analysiert den Code und fügt automatisch Abhängigkeiten zur `Cargo.toml`-Datei hinzu. Wenn eine Abhängigkeit im Code (`use crate`) verwendet wird, wird die entsprechende Bibliothek automatisch in die `Cargo.toml`-Datei eingefügt.

### 8. Git-Integration

Die Git-Integration ermöglicht es, Versionskontrollfunktionen direkt in der IDE auszuführen:

- **Commit erstellen**: Erstelle Commits über das Menü `Git -> Commit erstellen`.
- **Push/Pull**: Lade Änderungen in ein Remote-Repository hoch oder hole Änderungen von dort über `Git -> Push` bzw. `Git -> Pull`.
- **Branch-Verwaltung**: Erstelle neue Branches und wechsle zwischen Branches über `Git -> Neuen Branch erstellen` und `Git -> Branch wechseln`.
- **Git-Log anzeigen**: Zeige den Commit-Verlauf über `Git -> Git-Log anzeigen`.
- **Merge-Konflikte lösen**: Löse Merge-Konflikte über `Git -> Merge-Konflikte lösen`.

### 9. Projekt-Explorer

- Der Projekt-Explorer zeigt die Verzeichnisstruktur des Projekts an. Dateien können per Doppelklick im Editor geöffnet und bearbeitet werden. Außerdem können neue Dateien oder Ordner erstellt sowie gelöscht werden.

---
