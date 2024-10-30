import sys
from ambiance import Ambiance
from config_values import ConfigValues
from config_window import ConfigWindow
from PySide6 import QtCore, QtWidgets, QtGui


def main():
    app = QtWidgets.QApplication(['Funbiance']) 
    config_values = ConfigValues()
    config_window = ConfigWindow(config_values)
    config_window.show()
    ambiance = Ambiance(config_values)
    config_window.start_requested.connect(ambiance.on_start)
    config_window.stop_requested.connect(ambiance.on_stop)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()