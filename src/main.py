import sys
from ambiance import Ambiance
from config_values import ConfigValues
from config_window import ConfigWindow
from PySide6 import QtCore, QtWidgets, QtGui


def main():
    app = QtWidgets.QApplication([b'Funbiance']) 
    config_values = ConfigValues()
    config_window = ConfigWindow(config_values)
    ambiance = Ambiance(config_values)
    config_window.start.connect(ambiance.start)
    config_window.stop.connect(ambiance.stop)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()