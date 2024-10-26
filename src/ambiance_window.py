from PySide6.QtCore import QRect, Slot, Qt, QEvent, QThread
from PySide6.QtGui import QPainter, QWindow, QSurface, QOpenGLContext
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QPixmap, QPaintDevice, QBackingStore, QSurfaceFormat, QColor
from PySide6.QtOpenGL import QOpenGLFramebufferObject, QOpenGLWindow

class AmbianceWindow(QOpenGLWindow):

    def __init__(self, screen, **kwd):
        super().__init__(**kwd)
        self.pixmap = None
        
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
        self.requestUpdate()  # Request initial render
        
        self.color_count = 0

    @Slot(QPixmap)
    def set_pixmap(self, pixmap):
        print(f"Received pixmap in thread: {QThread.currentThread().objectName()}")
        print(f"Pixmap valid: {not pixmap.isNull() if pixmap else False}")       
        self.pixmap = pixmap
        if not self.pixmap:
            print("no pixmap")
        self.paintGL()
        
    def paintGL(self):
            
        try:
            painter = QPainter(self)
            try:
                if self.pixmap:
                    painter.drawPixmap(0, 0, self.width(), self.height(), self.pixmap)
                else:
                    painter.fillRect(0, 0, self.width(), self.height(), QColor.fromRgb(self.color_count, self.color_count, self.color_count))
                    self.color_count = (self.color_count + 1) % 255
                self.requestUpdate()
            finally:
                painter.end()
                
        except Exception as e:
            print(f"Render error: {e}")