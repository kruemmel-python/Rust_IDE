import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Früher Import
from gui.window import RustIDEWindow


def main():
    # Setze das OpenGL-Flag vor der Erstellung der QApplication
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    # Erstelle die QApplication-Instanz
    app = QApplication(sys.argv)
    
    # Erstelle das Hauptfenster
    window = RustIDEWindow()
    window.show()

    # Starte die Anwendung
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
