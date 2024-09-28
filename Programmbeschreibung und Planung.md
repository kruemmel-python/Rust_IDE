---

# **Rust IDE Präsentation**

## **1. Einführung**

Die Rust IDE ist eine umfassende Entwicklungsumgebung, die sich auf die Entwicklung von Rust-Projekten spezialisiert hat. Die IDE bietet eine Vielzahl an Funktionen, die sowohl Anfängern als auch erfahrenen Entwicklern die Arbeit mit Rust erleichtern. Mit integriertem Syntax-Highlighting, einem Plugin-System, Git-Integration, Debugger-Funktionen und KI-gestützter Codevervollständigung hebt sich die Rust IDE von klassischen Texteditoren ab und bietet eine echte Entwicklungsplattform für Rust-Projekte.

## **2. Überblick über die Hauptfunktionen**

### **2.1. Projektverwaltung**
- **Neues Projekt erstellen**: Über das Menü `Datei -> Neues Projekt` können neue Rust-Projekte erstellt werden. Die `Cargo.toml` wird dabei **automatisch generiert** und vorkonfiguriert.
- **Projekt öffnen**: Bereits bestehende Projekte können einfach geöffnet und über den Projekt-Explorer verwaltet werden.
- **Automatische Verwaltung der Cargo.toml**: Abhängigkeiten, die im Projekt durch `use`-Statements verwendet werden, werden **automatisch erkannt** und in die `Cargo.toml`-Datei eingetragen. Die IDE **erstellt und aktualisiert die Cargo.toml** je nach Nutzung der Bibliotheken und hält sie so immer auf dem aktuellen Stand. Zusätzliche Änderungen können ebenfalls direkt in der IDE vorgenommen werden.

### **2.2. Editor**
- **Syntax-Highlighting**: Der Editor unterstützt Rust-Syntax-Highlighting, das Schlüsselwörter, Kommentare und String-Literale farblich hervorhebt, um die Lesbarkeit des Codes zu verbessern.
- **Code-Vervollständigung mit KI**: Die IDE ist mit einer KI-basierten Codevervollständigung ausgestattet, die von Codestral unterstützt wird. Mit einem Klick wird der Code analysiert und automatisch vervollständigt.
- **Refactoring**: Mit einem Plugin können Codeelemente im gesamten Projekt umbenannt werden, was die Wartung und Weiterentwicklung erleichtert.

### **2.3. Build- und Debugging-Funktionen**
- **Build & Run**: Über das Menü `Build -> Build & Run` kann das aktuelle Projekt kompiliert und ausgeführt werden. Die Ergebnisse werden in der Konsole der IDE angezeigt.
- **Debugger**: Ein vollständig integrierter Debugger mit GDB-Unterstützung ermöglicht das Setzen von Breakpoints und die schrittweise Ausführung des Codes. Einfache Tastenkürzel erleichtern den Debugging-Prozess.
- **Clean Project**: Die `cargo clean`-Funktion kann einfach über das Menü aufgerufen werden, um Build-Artefakte zu entfernen.

### **2.4. Git-Integration**
- **Commit erstellen**: Direkte Git-Integration ermöglicht es, Änderungen am Code in Commits zu speichern und diese in ein Remote-Repository hochzuladen.
- **Branch-Verwaltung**: Entwickler können neue Branches erstellen und zwischen Branches wechseln, um verschiedene Features oder Fixes parallel zu entwickeln.
- **Git-Log anzeigen**: Der Commit-Verlauf kann in der IDE angezeigt werden, um den Fortschritt des Projekts zu verfolgen.

### **2.5. Layout-Anpassungen**
- **Schriftart und Schriftgröße ändern**: Über das Menü `Einstellungen -> Layout` können Schriftart und -größe für den Editor, die Konsole und den Projekt-Explorer angepasst werden.

## **3. Automatische Verwaltung der Cargo.toml**

Die Rust IDE bietet eine intelligente und automatische Verwaltung der **Cargo.toml**-Datei, die das zentrale Konfigurations- und Abhängigkeitsmanagement eines Rust-Projekts übernimmt.

### **3.1. Erstellung und Konfiguration**
Beim Erstellen eines neuen Projekts wird die `Cargo.toml` automatisch generiert. Die Standardprofile (z. B. Debug und Release) werden vorkonfiguriert, um eine optimale Arbeitsumgebung für Entwickler zu bieten. Zusätzlich können die Profile angepasst werden, z. B. durch Hinzufügen von speziellen Debugging-Optionen.

### **3.2. Automatische Erkennung von Abhängigkeiten**
Die IDE analysiert den Quellcode und erkennt automatisch, welche Bibliotheken über `use`-Statements importiert wurden. Diese Abhängigkeiten werden:

- **Dynamisch zur Cargo.toml hinzugefügt**: Jede erkannte Abhängigkeit wird mit ihrer neuesten Version aus dem Crates.io-Repository zur `Cargo.toml` hinzugefügt.
- **Automatisch aktualisiert**: Wenn neue Abhängigkeiten hinzugefügt oder bestehende entfernt werden, wird die `Cargo.toml` automatisch angepasst.

Dies eliminiert die Notwendigkeit, manuell nach Abhängigkeiten zu suchen und diese zur Konfigurationsdatei hinzuzufügen.

### **3.3. Verwaltung von Profilen**
Die IDE ermöglicht es, benutzerdefinierte Build-Profile in der `Cargo.toml` zu verwalten, z. B. für optimierte Release-Builds oder spezielle Debug-Builds. Diese Profile werden automatisch bei der Projekterstellung hinzugefügt und können bei Bedarf angepasst werden.

## **4. Plugin-System**

Die Rust IDE verfügt über ein flexibles Plugin-System, das es Entwicklern ermöglicht, die IDE mit benutzerdefinierten Erweiterungen zu versehen. Plugins können schnell hinzugefügt und im Plugin-Menü verwaltet werden, ohne dass der Kern der IDE verändert werden muss.

### **4.1. Verfügbare Plugins**

#### **4.1.1. Documentation Generator Plugin**
Dieses Plugin generiert automatisch die Dokumentation für das aktuelle Projekt. Es überwacht Code-Änderungen und erstellt die Dokumentation über `cargo doc`. Die Dokumentation wird direkt in einem integrierten Browser-Tab angezeigt.

#### **4.1.2. Rust Code Formatter Plugin**
Das Rust Code Formatter Plugin verwendet `rustfmt`, um den Code automatisch zu formatieren und ihn lesbarer zu machen. Es wird sichergestellt, dass der Code den Rust-Konventionen entspricht.

#### **4.1.3. Hover with Quickfix Plugin**
Dieses Plugin zeigt beim Überfahren von Codeelementen hilfreiche Quickfixes und Dokumentationen an. Mit einem Rechtsklick auf das Codeelement können weitere Optionen wie Codebeispiele oder Erklärungen über die Codestral-API abgerufen werden.

#### **4.1.4. Refactor Plugin**
Das Refactor Plugin ermöglicht es, Codeelemente wie Variablen oder Funktionen schnell und einfach umzubenennen. Der gesamte Code wird automatisch aktualisiert, um Refactorings effizient umzusetzen.

#### **4.1.5. Unittest Plugin**
Mit dem Unittest Plugin können Entwickler die Unittests des Projekts direkt aus der IDE heraus ausführen. Es zeigt die Testergebnisse in der Konsole an und ermöglicht eine schnelle Fehlerbehebung.

## **5. Benutzeroberfläche**

Die Rust IDE bietet eine intuitive Benutzeroberfläche, die aus mehreren Komponenten besteht:

- **Editor**: Der Editor unterstützt mehrere Tabs, sodass Entwickler an mehreren Dateien gleichzeitig arbeiten können.
- **Projekt-Explorer**: Die Verzeichnisstruktur des Projekts wird im Projekt-Explorer angezeigt, Dateien können per Doppelklick im Editor geöffnet werden.
- **Konsole**: Die Konsole zeigt Build-, Debug- und Test-Ausgaben an. Sie dient zur Fehleranalyse und Überwachung der Ausgaben des Projekts.
- **Menüleiste**: Über die Menüleiste können verschiedene Funktionen der IDE genutzt werden, wie etwa das Erstellen eines neuen Projekts, das Ausführen von Builds oder das Verwalten von Git-Vorgängen.

## **6. Installation und Einrichtung**

### **6.1. Rust und Abhängigkeiten**
Um die IDE nutzen zu können, müssen Rust und einige Abhängigkeiten installiert werden:

1. Rust Installation:
    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

2. Python und PyQt5 für die Benutzeroberfläche:
    ```bash
    pip install PyQt5 toml requests pyperclip
    ```

3. **Visual Studio Build Tools** (für Windows-Benutzer) für die MSVC-Toolchain.

### **6.2. Starten der IDE**
Nach der Einrichtung der Abhängigkeiten kann die IDE durch das Ausführen des Python-Skripts gestartet werden:
```bash
python main.py
```

## **7. Zukünftige Erweiterungen und Verbesserungsvorschläge**

Während die Rust IDE bereits viele wichtige Funktionen unterstützt, gibt es mehrere Erweiterungen, die die Benutzerfreundlichkeit und Funktionalität noch weiter verbessern könnten:

### **7.1. Verbesserte Debugging-Funktionalität**
- **Breakpoint-Management**: Integration eines visuellen Breakpoint-Systems, das Breakpoints direkt im Editor anzeigt und es ermöglicht, diese einfach durch einen Klick auf die Seitenleiste zu setzen oder zu entfernen.
- **Debugger-Kontrollfenster**: Ein spezielles Fenster, das den aktuellen Status der Variablen während der Debugging-Sitzung anzeigt, wäre hilfreich.

### **7.2. Erweiterte Refactoring-Optionen**
- **Extract Function**: Eine Funktion, die es ermöglicht, ausgewählten Code in eine neue Funktion zu extrahieren.
- **Code-Vorschau vor Refactoring**: Vorschläge anzeigen, bevor Refactoring-Aktionen übernommen werden.

### **7.3. Erweiter

te Code-Vervollständigung**
- **Kontextbasierte Vervollständigung**: Verbesserung der KI-Codevervollständigung, indem nicht nur einfache Vorschläge, sondern auch kontextbezogene Vorschläge auf Basis des gesamten Projekts angeboten werden.

### **7.4. Profiling-Tool**
- **Integriertes Profiling**: Ein Tool zur Performance-Analyse, um den Code auf Laufzeitprobleme zu untersuchen und Optimierungen zu identifizieren.

### **7.5. Testabdeckung**
- **Testabdeckung messen**: Eine Funktion, die die Testabdeckung des Codes misst und Bereiche identifiziert, die nicht ausreichend getestet wurden.

---
