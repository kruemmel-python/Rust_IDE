# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui.window import RustIDEWindow

def main():
    app = QApplication(sys.argv)
    window = RustIDEWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
