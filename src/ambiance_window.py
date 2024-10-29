from PySide6.QtCore import QRect, Slot, Qt, QEvent, QThread
from PySide6.QtGui import QPainter, QWindow, QSurface, QOpenGLContext
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QPixmap, QPaintDevice, QBackingStore, QSurfaceFormat, QColor, QScreen
from PySide6.QtOpenGL import QOpenGLFramebufferObject, QOpenGLWindow

from capture_pipeline import CapturePipeline

class AmbianceWindow(QOpenGLWindow):

    def __init__(self, screen: QScreen, *, capture: CapturePipeline=None, **kwd):
        super().__init__(QOpenGLWindow.UpdateBehavior.NoPartialUpdate, **kwd)
        self._pixmap = None
        self._capture = capture
        
        self.setScreen(screen)
        
        # Create the window with proper geometry
        geometry = screen.geometry()
        print(f"geometry: {geometry}")
        self.setGeometry(geometry)
        
        surfaceFormat = QSurfaceFormat()
        surfaceFormat.setSwapInterval(1)
        self.setFormat(surfaceFormat)
        
        # Make sure window is visible and on top
        self.setFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.create()  # Ensure native window is created
        self.show()
        # self.requestUpdate()  # Request initial render
        
        self.color_count = 0

    @Slot(QPixmap)
    def on_next_pixmap(self, pixmap):
        self._pixmap = pixmap
        self.update()
        
    def paintEvent(self, event):
            
        try:
            painter = QPainter(self)

            try:
                painter.setRenderHints(QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.Antialiasing)
                pixmap = self._pixmap if not self._capture else self._capture._pixmap
                if pixmap:
                    painter.drawPixmap(0, 0, self.width(), self.height(), pixmap)
                else:
                    painter.fillRect(0, 0, self.width(), self.height(), QColor.fromRgb(self.color_count, self.color_count, self.color_count))
                    self.color_count = (self.color_count + 1) % 255  # animate for debug
                
            finally:
                painter.end()
                
        except Exception as e:
            print(f"Render error: {e}")