import sys
from capture_pipeline import CapturePipeline
from config_values import ConfigValues
from config_window import ConfigWindow
from PySide6 import QtCore, QtWidgets, QtGui


def main():
    app = QtWidgets.QApplication([]) 
    config_values = ConfigValues()
    ambiance_window = CapturePipeline(config_values)
    config_window = ConfigWindow(config_values, ambiance_window)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()