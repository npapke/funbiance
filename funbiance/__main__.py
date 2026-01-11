import sys
from .ambiance import Ambiance
from .config_values import ConfigValues
from .config_window import ConfigWindow
from PySide6 import QtCore, QtWidgets, QtGui
import logging


class SpamFilter(logging.Filter):
    def filter(self, record):
        # Filter out the color setting spam from the hue library
        if "Setting color" in record.getMessage() and record.name == "root":
            return False
        return True


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),  # Console output
            logging.FileHandler("funbiance.log")  # File output
        ]
    ) 
    
    # Add spam filter to root logger
    logging.getLogger().addFilter(SpamFilter())
    logger = logging.getLogger(__name__)
    logger.info('Starting funbiance')
    
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