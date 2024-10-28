import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: configWindow
    width: 300
    height: 600
    title: "Funbiance Config Window"
    visible: true

    // Signals to be exposed to backend
    signal saveConfig()
    signal startClicked()
    signal stopClicked()

    // Set the window background to match system theme
    SystemPalette { id: systemPalette }
    color: systemPalette.window


    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        // Blur Factor Controls
        Label {
            text: "Blur Factor (0-100)"
        }

        RowLayout {
            Slider {
                id: blurFactorSlider
                Layout.fillWidth: true
                from: 0
                to: 100
                stepSize: 1
                value: configValues.blur_factor
                onValueChanged: {
                    blurFactorInput.text = value
                    configValues.blur_factor = value
                }
            }

            TextField {
                id: blurFactorInput
                Layout.preferredWidth: 50
                text: blurFactorSlider.value
                validator: IntValidator { bottom: 0; top: 100 }
                onEditingFinished: {
                    if (text >= 0 && text <= 100) {
                        blurFactorSlider.value = parseInt(text)
                    }
                }
            }
        }

        // Brightness Controls
        Label {
            text: "Brightness:"
        }

        RowLayout {
            Slider {
                id: brightnessSlider
                Layout.fillWidth: true
                from: 0
                to: 100
                stepSize: 1
                value: configValues.brightness
                onValueChanged: {
                    brightnessInput.text = value
                    configValues.brightness = value
                }
            }

            TextField {
                id: brightnessInput
                Layout.preferredWidth: 50
                text: brightnessSlider.value
                validator: IntValidator { bottom: 0; top: 100 }
                onEditingFinished: {
                    if (text >= 0 && text <= 100) {
                        brightnessSlider.value = parseInt(text)
                    }
                }
            }
        }

        // Number of Windows Controls
        Label {
            text: "Number of Windows (0-6)"
        }

        RowLayout {
            Slider {
                id: numWindowsSlider
                Layout.fillWidth: true
                from: 0
                to: 6
                stepSize: 1
                value: configValues.num_windows
                onValueChanged: {
                    numWindowsInput.text = value
                    configValues.num_windows = value
                }
            }

            TextField {
                id: numWindowsInput
                Layout.preferredWidth: 50
                text: numWindowsSlider.value
                validator: IntValidator { bottom: 0; top: 6 }
                onEditingFinished: {
                    if (text >= 0 && text <= 6) {
                        numWindowsSlider.value = parseInt(text)
                    }
                }
            }
        }

        // Bridge Address
        Label {
            text: "Hue Bridge Address"
        }

        TextField {
            id: bridgeAddressInput
            Layout.fillWidth: true
            text: configValues.hue_bridge_address
            onTextChanged: configValues.bridge_address = text
        }

        // Bridge Username
        Label {
            text: "Hue Bridge Username"
        }

        TextField {
            id: bridgeUsernameInput
            Layout.fillWidth: true
            text: configValues.hue_bridge_username
            onTextChanged: configValues.bridge_username = text
        }

        // Hue Min Brightness
        Label {
            text: "Hue Min Brightness"
        }

        RowLayout {
            Slider {
                id: hueMinBrightnessSlider
                Layout.fillWidth: true
                from: 1
                to: 254
                stepSize: 1
                value: configValues.hue_min_brightness
                onValueChanged: {
                    hueMinBrightnessInput.text = value
                    configValues.hue_min_brightness = value
                }
            }

            TextField {
                id: hueMinBrightnessInput
                Layout.preferredWidth: 50
                text: hueMinBrightnessSlider.value
                validator: IntValidator { bottom: 1; top: 254 }
                onEditingFinished: {
                    if (text >= 1 && text <= 254) {
                        hueMinBrightnessSlider.value = parseInt(text)
                    }
                }
            }
        }

        // Hue Max Brightness
        Label {
            text: "Hue Max Brightness"
        }

        RowLayout {
            Slider {
                id: hueMaxBrightnessSlider
                Layout.fillWidth: true
                from: 1
                to: 254
                stepSize: 1
                value: configValues.hue_max_brightness
                onValueChanged: {
                    hueMaxBrightnessInput.text = value
                    configValues.hue_max_brightness = value
                }
            }

            TextField {
                id: hueMaxBrightnessInput
                Layout.preferredWidth: 50
                text: hueMaxBrightnessSlider.value
                validator: IntValidator { bottom: 1; top: 254 }
                onEditingFinished: {
                    if (text >= 1 && text <= 254) {
                        hueMaxBrightnessSlider.value = parseInt(text)
                    }
                }
            }
        }

        // Buttons
        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            Button {
                text: "Save"
                Layout.fillWidth: true
                onClicked: configWindow.saveConfig()
            }

            Button {
                text: "Run"
                Layout.fillWidth: true
                onClicked: configWindow.startClicked()
            }

            Button {
                text: "Stop"
                Layout.fillWidth: true
                onClicked: configWindow.stopClicked()
            }
        }

        // Spacer
        Item {
            Layout.fillHeight: true
        }
    }
}
