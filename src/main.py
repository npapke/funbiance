import sys
from config_window import ConfigWindow
from PySide6 import QtCore, QtWidgets, QtGui


def main():
    app = QtWidgets.QApplication([]) 
    config_window = ConfigWindow()   
    config_window.resize(800, 600)
    config_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()