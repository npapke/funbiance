from PySide6.QtCore import QObject, Slot, Qt
from PySide6.QtWidgets import QApplication

from ambiance_window import AmbianceWindow
from capture_pipeline import CapturePipeline

class Ambiance(QObject):
    
    def __init__(self, configuration_values):
        self._config = configuration_values
        self.capture = None
        self.windows = []
        
    @Slot()
    def start(self):
        if self.capture is None:
            self.capture = CapturePipeline(self._config)

            app = QApplication.instance()
            for screen in app.screens():
                if screen != app.primaryScreen():
                    print(f"Avail Geometry: {screen.availableGeometry()}")
                    w = AmbianceWindow(screen, capture=self.capture)
                    self.capture.frame_sample.connect(w.set_pixmap, Qt.ConnectionType.QueuedConnection)
                    self.windows.append(w)
                    
                    break
                    
            self.capture.run()
 
    @Slot()
    def stop(self):
        if self.capture is not None:
            self.capture.terminate()
            self.capture = None
            
            for w in self.windows:
                w.close()
                del w
            self.windows = []
    