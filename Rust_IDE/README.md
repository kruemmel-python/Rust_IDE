
---

# Rust IDE

Eine umfassende Entwicklungsumgebung f�r Rust, die alle wesentlichen Funktionen zur Entwicklung, Erstellung und zum Debuggen von Rust-Projekten bietet. Die IDE unterst�tzt das Erstellen neuer Rust-Projekte, das �ffnen bestehender Projekte, die Verwaltung von Abh�ngigkeiten �ber die `Cargo.toml` und bietet einen integrierten Debugger. Zus�tzlich gibt es erweiterte Funktionen wie **Git-Integration**, **KI-Codevervollst�ndigung** und **Layout-Anpassungen**.

## Installation

### Rust installieren

Um die Rust-Entwicklungsumgebung auf deinem System zu installieren, f�hre den folgenden Befehl im Terminal oder der Eingabeaufforderung aus:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Dieser Befehl installiert Rust, `cargo` (das Build-System und Paketmanagement-Tool von Rust) sowie das Tool `rustup` zur Verwaltung von Toolchains.

### Installation der Windows-Toolchain

Falls du auf Windows arbeitest, wirst du auch die **Visual Studio Build Tools** ben�tigen, um Rust mit der MSVC-Toolchain zu verwenden.

1. Lade die **Visual Studio Build Tools** herunter und installiere sie von der folgenden Webseite:
   [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

2. W�hle w�hrend der Installation die Option "Desktop development with C++" aus.

3. Nach der Installation kannst du sicherstellen, dass Rust die richtige Toolchain verwendet, indem du den folgenden Befehl ausf�hrst:

```bash
rustup default stable-x86_64-pc-windows-msvc
```

### Python und Abh�ngigkeiten

Zus�tzlich zu Rust ben�tigst du Python und einige Python-Bibliotheken, um die IDE auszuf�hren:

```bash
pip install PyQt5 toml requests pyperclip
```

## Anwendungshinweise

- **Projekt erstellen**: W�hle `Datei -> Neues Projekt`, um ein neues Rust-Projekt zu erstellen.
- **Projekt �ffnen**: �ffne ein bestehendes Rust-Projekt �ber `Datei -> Projekt �ffnen`.
- **Build & Run**: Verwende `Ctrl+B`, um das aktuelle Projekt zu kompilieren und auszuf�hren.
- **Debugger**: Nutze die integrierten Debugger-Funktionen, um Haltepunkte zu setzen und den Programmablauf zu steuern.
- **Code vervollst�ndigen**: �ber `Code -> Code vervollst�ndigen` kannst du die KI nutzen, um den aktuellen Code automatisch vervollst�ndigen zu lassen.
- **Layout �ndern**: Passe �ber `Einstellungen -> Layout` die Schriftgr��e und den Schriftstil im Editor an.
- **Git-Integration**: Erstelle Commits, push/pull zu einem Remote-Repository oder wechsle Branches direkt �ber das `Git`-Men�.

## Funktionen

### 1. Projektverwaltung

- **Neues Projekt erstellen**: �ber das Men� `Datei -> Neues Projekt` kann ein neues Rust-Projekt erstellt werden. Die `Cargo.toml` wird automatisch erstellt und konfiguriert.
- **Projekt �ffnen**: Bestehende Projekte k�nnen �ber `Datei -> Projekt �ffnen` geladen werden. Der Projektbaum wird im Explorer angezeigt, und Dateien k�nnen durch Doppelklick im Editor bearbeitet werden.
- **Cargo.toml �ffnen**: Die `Cargo.toml`-Datei des Projekts kann �ber `Datei -> Cargo.toml �ffnen` bearbeitet werden. Abh�ngigkeiten werden automatisch hinzugef�gt, basierend auf dem Code im Projekt.
- **Projekt speichern**: Speichert die aktuell im Editor ge�ffnete Datei �ber `Datei -> Projekt speichern`. Abh�ngigkeiten werden automatisch erkannt und in der `Cargo.toml`-Datei aktualisiert.

### 2. Editor

- **Syntax-Highlighting**: Der integrierte Editor unterst�tzt Rust-Syntax-Highlighting f�r Schl�sselw�rter, Kommentare und Strings.
- **Code-Vervollst�ndigung mit KI**: Der Editor ist mit einer **KI-basierten Codevervollst�ndigung** (via Codestral) ausgestattet. Der Code kann automatisch erg�nzt werden, indem du im Men� `Code -> Code vervollst�ndigen` ausw�hlst.

### 3. Build- und Run-Funktionen

- **Build & Run**: �ber das Men� `Build -> Build & Run` oder den Shortcut `Ctrl + B` kann das Projekt kompiliert und ausgef�hrt werden. Der Fortschritt und die Ausgabe werden im unteren Ausgabefenster der IDE angezeigt.
- **Clean Project**: Bereinigt das Projektverzeichnis von Build-Artefakten �ber `Build -> Clean Project` oder den Shortcut `Ctrl + Shift + C`.

### 4. Build-Modus wechseln

- Wechsle zwischen Debug- und Release-Modus im Men� `Build-Modus`. Der Debug-Modus erstellt das Projekt mit zus�tzlichen Debugging-Informationen, w�hrend der Release-Modus f�r optimale Leistung optimiert ist.

### 5. Debugger

Das Debugging-Men� ist vollst�ndig in die IDE integriert. Es verwendet GDB zur Untersuchung des Programmablaufs, setzt Haltepunkte und bietet die M�glichkeit, den Code schrittweise zu durchlaufen.

- **Start Debugger (`Ctrl+D`)**: Startet den Debugger im Debug-Modus.
- **Run Debugger (`Ctrl+R`)**: Startet das Programm im Debugger.
- **Set Breakpoint (main) (`Ctrl+Shift+B`)**: Setzt einen Haltepunkt in der `main`-Funktion.
- **Step (`F10`)**: F�hrt einen Einzelschritt im Debugger aus.
- **Next (`F11`)**: Springt zum n�chsten Schritt im Code.
- **Continue (`F5`)**: Setzt die Ausf�hrung im Debugger fort.
- **Quit Debugger (`Ctrl+Q`)**: Beendet die Debugger-Sitzung.

### 6. Layout-Anpassungen

�ber das Men� `Einstellungen -> Layout` kannst du die Schriftart und -gr��e im Editor anpassen. Diese Funktion bietet Flexibilit�t bei der Gestaltung der Arbeitsumgebung und verbessert die Lesbarkeit.

### 7. Projekt-Abh�ngigkeiten

- Die IDE analysiert den Code und f�gt automatisch Abh�ngigkeiten zur `Cargo.toml`-Datei hinzu. Wenn eine Abh�ngigkeit im Code (`use crate`) verwendet wird, wird die entsprechende Bibliothek automatisch in die `Cargo.toml`-Datei eingef�gt.

### 8. Git-Integration

Die Git-Integration erm�glicht es, Versionskontrollfunktionen direkt in der IDE auszuf�hren:

- **Commit erstellen**: Erstelle Commits �ber das Men� `Git -> Commit erstellen`.
- **Push/Pull**: Lade �nderungen in ein Remote-Repository hoch oder hole �nderungen von dort �ber `Git -> Push` bzw. `Git -> Pull`.
- **Branch-Verwaltung**: Erstelle neue Branches und wechsle zwischen Branches �ber `Git -> Neuen Branch erstellen` und `Git -> Branch wechseln`.
- **Git-Log anzeigen**: Zeige den Commit-Verlauf �ber `Git -> Git-Log anzeigen`.
- **Merge-Konflikte l�sen**: L�se Merge-Konflikte �ber `Git -> Merge-Konflikte l�sen`.

### 9. Projekt-Explorer

- Der Projekt-Explorer zeigt die Verzeichnisstruktur des Projekts an. Dateien k�nnen per Doppelklick im Editor ge�ffnet und bearbeitet werden. Au�erdem k�nnen neue Dateien oder Ordner erstellt sowie gel�scht werden.

---
