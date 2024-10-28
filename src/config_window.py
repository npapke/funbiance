from PySide6.QtWidgets import (QWidget, QVBoxLayout, QSlider, QLabel, 
                              QHBoxLayout, QPushButton, QLineEdit)
from PySide6.QtCore import Qt, Signal, QObject, QCoreApplication
from PySide6.QtGui import QIntValidator
from PySide6.QtQml import QQmlApplicationEngine


class ConfigWindow(QObject):
    
    start_requested = Signal()
    stop_requested = Signal()
 
    
    def __init__(self, config_values):
        super().__init__()
        self._config = config_values
        
        self.engine = QQmlApplicationEngine()
        print(self.engine.importPathList())
    
        # Create and expose ConfigValues to QML
        self.engine.rootContext().setContextProperty("configValues", self._config)
        
        # Load QML file
        self.engine.load("src/config_window.qml")
        
        if self.engine.rootObjects():
            self.window = self.engine.rootObjects()[0]
            
            self.window.startClicked.connect(self.start_requested.emit)
            self.window.stopClicked.connect(self.stop_requested.emit)
            self.window.saveConfig.connect(self._config.save)
            
            self.window.show()
        else:
            self.window = None
            print("Unable to create ConfigWindow")
            
    def show(self):
        if self.window:
            self.window.show()

    def hide(self):
        if self.window:
            self.window.hide()
 
