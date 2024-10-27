from PySide6.QtCore import QObject, Slot, Qt
from PySide6.QtWidgets import QApplication

from ambiance_hue import AmbianceHue
from ambiance_window import AmbianceWindow
from capture_pipeline import CapturePipeline

class Ambiance(QObject):
    
    def __init__(self, configuration_values):
        self._config = configuration_values
        self.capture = None
        self.windows = []
        
    @Slot()
    def on_start(self):
        if self.capture is None:
            self.capture = CapturePipeline(self._config)
            self.capture.pipeline_active.connect(self.on_capture_active)
            self.capture.run()

            
    @Slot()
    def on_capture_active(self):
        app = QApplication.instance()
        for screen in app.screens():
            if screen != app.primaryScreen():
                print(f"Avail Geometry: {screen.availableGeometry()}")
                w = AmbianceWindow(screen)
                self.capture.frame_sample.connect(w.on_next_pixmap, Qt.ConnectionType.QueuedConnection)
                self.windows.append(w)
                
                # break # TODO remove
            
        self.hue = AmbianceHue(self._config)
        self.capture.color_sample.connect(self.hue.set_color, Qt.ConnectionType.QueuedConnection)
                
    @Slot()
    def on_stop(self):
        if self.capture is not None:
            
            for w in self.windows:
                w.close()
                del w
            self.windows = []
            
            self.capture.terminate()
            del self.capture
            self.capture = None