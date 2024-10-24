from PySide6.QtWidgets import (QWidget, QVBoxLayout, QSlider, QLabel, 
                              QHBoxLayout, QPushButton, QLineEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator

class ConfigWindow(QWidget):
    def __init__(self, config_values, ambiance_window):
        super().__init__()
        self.config_values = config_values
        self.ambiance_window = ambiance_window
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Config Window')

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Blur Factor Controls
        blurFactorLabel = QLabel('Blur Factor (0-100)')
        layout.addWidget(blurFactorLabel)

        blurControlLayout = QHBoxLayout()
        layout.addLayout(blurControlLayout)

        self.blurFactorSlider = QSlider(Qt.Horizontal)
        self.blurFactorSlider.setMinimum(0)
        self.blurFactorSlider.setMaximum(100)
        self.blurFactorSlider.setValue(self.config_values.blur_factor)
        self.blurFactorSlider.setTickInterval(10)
        self.blurFactorSlider.setTickPosition(QSlider.TicksBelow)
        blurControlLayout.addWidget(self.blurFactorSlider)

        self.blurFactorText = QLineEdit()
        self.blurFactorText.setValidator(QIntValidator(0, 100))
        self.blurFactorText.setMaximumWidth(50)
        self.blurFactorText.setText(str(self.config_values.blur_factor))
        blurControlLayout.addWidget(self.blurFactorText)

        # Number of Windows Controls
        numWindowsLabel = QLabel('Number of Windows (0-6)')
        layout.addWidget(numWindowsLabel)

        numWindowsControlLayout = QHBoxLayout()
        layout.addLayout(numWindowsControlLayout)

        self.numWindowsSlider = QSlider(Qt.Horizontal)
        self.numWindowsSlider.setMinimum(0)
        self.numWindowsSlider.setMaximum(6)
        self.numWindowsSlider.setValue(self.config_values.num_windows)
        self.numWindowsSlider.setTickInterval(1)
        self.numWindowsSlider.setTickPosition(QSlider.TicksBelow)
        numWindowsControlLayout.addWidget(self.numWindowsSlider)

        self.numWindowsText = QLineEdit()
        self.numWindowsText.setValidator(QIntValidator(0, 6))
        self.numWindowsText.setMaximumWidth(50)
        self.numWindowsText.setText(str(self.config_values.num_windows))
        numWindowsControlLayout.addWidget(self.numWindowsText)
        # Connect signals
        self.blurFactorSlider.valueChanged.connect(self.onBlurFactorSliderChanged)
        self.blurFactorText.editingFinished.connect(self.onBlurFactorTextChanged)
        self.numWindowsSlider.valueChanged.connect(self.onNumWindowsSliderChanged)
        self.numWindowsText.editingFinished.connect(self.onNumWindowsTextChanged)

        # Buttons
        buttonBox = QHBoxLayout()
        layout.addLayout(buttonBox)

        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.onSaveClicked)
        buttonBox.addWidget(saveButton)

        runButton = QPushButton('Run')
        runButton.clicked.connect(self.onRunClicked)
        buttonBox.addWidget(runButton)

        stopButton = QPushButton('Stop')
        stopButton.clicked.connect(self.onStopClicked)
        buttonBox.addWidget(stopButton)

        self.show()

    def onBlurFactorSliderChanged(self, value):
        self.blurFactorText.setText(str(value))
        self.config_values.blur_factor = value

    def onBlurFactorTextChanged(self):
        try:
            value = int(self.blurFactorText.text())
            if 0 <= value <= 100:
                self.blurFactorSlider.setValue(value)
                self.config_values.blur_factor = value
        except ValueError:
            # Restore the text to match the slider if invalid input
            self.blurFactorText.setText(str(self.blurFactorSlider.value()))

    def onNumWindowsSliderChanged(self, value):
        self.numWindowsText.setText(str(value))
        self.config_values.num_windows = value

    def onNumWindowsTextChanged(self):
        try:
            value = int(self.numWindowsText.text())
            if 0 <= value <= 6:
                self.numWindowsSlider.setValue(value)
                self.config_values.num_windows = value
        except ValueError:
            # Restore the text to match the slider if invalid input
            self.numWindowsText.setText(str(self.numWindowsSlider.value()))

    def onSaveClicked(self):
        self.config_values.save()

    def onRunClicked(self):
        self.ambiance_window.run()

    def onStopClicked(self):
        self.ambiance_window.terminate()