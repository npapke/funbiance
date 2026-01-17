from PySide6.QtCore import QRect, Slot, Qt, QEvent, QThread, QTime
from PySide6.QtGui import QPainter, QWindow, QSurface, QOpenGLContext
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QPixmap, QPaintDevice, QBackingStore, QSurfaceFormat, QColor, QScreen, QFont
from PySide6.QtOpenGL import QOpenGLFramebufferObject, QOpenGLWindow
import logging

from .capture_pipeline import CapturePipeline

logger = logging.getLogger(__name__)

class AmbianceWindow(QOpenGLWindow):

    def __init__(self, screen: QScreen, *, capture: CapturePipeline=None, **kwd) -> None:
        super().__init__(QOpenGLWindow.UpdateBehavior.NoPartialUpdate, **kwd)
        self._pixmap = None
        self._capture = capture
        
        self.setScreen(screen)
        geometry = screen.geometry()
        logger.info(f"geometry: {geometry}")
        self.setGeometry(geometry)
        
        surfaceFormat = QSurfaceFormat()
        surfaceFormat.setSwapInterval(1)
        self.setFormat(surfaceFormat)
        
        # self.setFlags(Qt.WindowType.WindowStaysOnTopHint ) #| Qt.WindowType.FramelessWindowHint)
        # self.setFlags(Qt.WindowType.MaximizeUsingFullscreenGeometryHint ) #| Qt.WindowType.FramelessWindowHint)

        self.create()  # Ensure native window is created
        self.showFullScreen()
        # self.show()
        
        # Force the window to the correct screen (workaround for KDE issues)
        if self.screen() != screen:
            logger.warning(f"Window on wrong screen, moving from {self.screen().name()} to {screen.name()}")
            self.setScreen(screen)
            self.setGeometry(screen.geometry())

        self.color_count = 0
        self.dominant_color = QColor.fromRgb(0,0,0)
        

    @Slot(QPixmap)
    def on_next_pixmap(self, pixmap) -> None:
        self._pixmap = pixmap
        self.update()
        
    @Slot(int, int, int)
    def set_color(self, r: int, g: int, b: int) -> None:
        self.dominant_color = QColor.fromRgb(r, g, b)
        
    def paintEvent(self, event) -> None:
            
        try:
            painter = QPainter(self)

            try:
                painter.setRenderHints(QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.Antialiasing)
                pixmap = self._pixmap if not self._capture else self._capture._pixmap
                if pixmap:
                    painter.drawPixmap(0, 0, self.width(), self.height(), pixmap)
                    
                    # Debug swatch for Hue
                    # painter.fillRect(self.width() / 3, self.height()/ 3 * 2, self.width() / 3, self.height() / 4, self.dominant_color)
                else:
                    painter.fillRect(0, 0, self.width(), self.height(), QColor.fromRgb(self.color_count, self.color_count, self.color_count))
                    self.color_count = (self.color_count + 1) % 255  # animate for debug
                
                # Draw current time in corner
                current_time = QTime.currentTime().toString("hh:mm:ss")
                painter.setPen(QColor.fromRgb(255, 255, 255))  # White text
                font = QFont("Monospace", 24)
                font.setStyleHint(QFont.StyleHint.Monospace)
                painter.setFont(font)
                
                # Draw in bottom-right corner with some padding
                text_rect = painter.fontMetrics().boundingRect(current_time)
                padding = 20
                painter.drawText(
                    self.width() - text_rect.width() - padding,
                    self.height() - text_rect.height() - padding,
                    current_time
                )

            finally:
                painter.end()
                
        except Exception as e:
            logger.warning(f"Render error: {e}")