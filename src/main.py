import sys
from config_values import ConfigValues
from config_window import ConfigWindow
from PySide6 import QtCore, QtWidgets, QtGui


def main():
    app = QtWidgets.QApplication([]) 
    config_values = ConfigValues()
    config_window = ConfigWindow(config_values)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()