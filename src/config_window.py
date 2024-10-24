from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

class ConfigWindow(QWidget):
    def __init__(self, config_values):
        super().__init__()
        self.config_values = config_values
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Config Window')

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Slider for "Blur Factor"
        self.blurFactorSlider = QSlider(Qt.Horizontal)
        self.blurFactorSlider.setMinimum(0)
        self.blurFactorSlider.setMaximum(100)
        self.blurFactorSlider.setValue(self.config_values.blur_factor)  # Initialize from config
        self.blurFactorSlider.setTickInterval(10)
        self.blurFactorSlider.setTickPosition(QSlider.TicksBelow)
        self.blurFactorSlider.valueChanged.connect(self.onBlurFactorChanged)

        blurFactorLabel = QLabel('Blur Factor (0-100)')
        layout.addWidget(blurFactorLabel)
        layout.addWidget(self.blurFactorSlider)

        # Slider for "Number of Windows"
        self.numWindowsSlider = QSlider(Qt.Horizontal)
        self.numWindowsSlider.setMinimum(0)
        self.numWindowsSlider.setMaximum(6)
        self.numWindowsSlider.setValue(self.config_values.num_windows)  # Initialize from config
        self.numWindowsSlider.setTickInterval(1)
        self.numWindowsSlider.setTickPosition(QSlider.TicksBelow)
        self.numWindowsSlider.valueChanged.connect(self.onNumWindowsChanged)

        numWindowsLabel = QLabel('Number of Windows (0-6)')
        layout.addWidget(numWindowsLabel)
        layout.addWidget(self.numWindowsSlider)

        # Buttons
        buttonBox = QHBoxLayout()
        layout.addLayout(buttonBox)

        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.onSaveClicked)
        buttonBox.addWidget(saveButton)

        runButton = QPushButton('Run')
        buttonBox.addWidget(runButton)

        self.show()

    def onBlurFactorChanged(self, value):
        self.config_values.blur_factor = value

    def onNumWindowsChanged(self, value):
        self.config_values.num_windows = value

    def onSaveClicked(self):
        self.config_values.save()
