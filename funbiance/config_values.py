import os
import json
from PySide6.QtCore import QObject, Property, Signal
from appdirs import user_data_dir

class ConfigValues(QObject):
    # Define signals for property changes
    blurFactorChanged = Signal(int)
    brightnessChanged = Signal(int)
    hueBridgeAddressChanged = Signal(str)
    hueBridgeUsernameChanged = Signal(str)
    hueBridgeClientkeyChanged = Signal(str)
    hueMinBrightnessChanged = Signal(int)
    hueMaxBrightnessChanged = Signal(int)
    hueSaturationChanged = Signal(int)

    def __init__(self):
        super().__init__()
        # Initialize private variables
        self._blur_factor_value = 50
        self._brightness_value = 50
        self._hue_bridge_address_value = ''
        self._hue_bridge_username_value = ''
        self._hue_bridge_clientkey_value = ''
        self._hue_min_brightness_value = 1
        self._hue_max_brightness_value = 254
        self._hue_saturation_value = 1.0

        # Get the appropriate XDG directory for storing user data
        dir_path = user_data_dir("Funbiance", roaming=True)

        # Create the directory if it doesn't already exist
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        # Set the filepath for the saved configuration file
        self._filename = os.path.join(dir_path, "funbiance.json")

        # Load the saved configuration file if it exists
        if os.path.isfile(self._filename):
            self.load()

    # Blur Factor
    @Property(int, notify=blurFactorChanged)
    def blur_factor(self):
        return self._blur_factor_value

    @blur_factor.setter
    def blur_factor(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Blur factor must be a number")
        value = int(value)
        if not 0 <= value <= 100:
            raise ValueError("Blur factor out of range (0-100)")
        if self._blur_factor_value != value:
            self._blur_factor_value = value
            self.blurFactorChanged.emit(value)

    # Brightness
    @Property(int, notify=brightnessChanged)
    def brightness(self):
        return self._brightness_value

    @brightness.setter
    def brightness(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Brightness must be a number")
        value = int(value)
        if not 0 <= value <= 100:
            raise ValueError("Brightness out of range (0-100)")
        if self._brightness_value != value:
            self._brightness_value = value
            self.brightnessChanged.emit(value)

    # Hue Bridge Address
    @Property(str, notify=hueBridgeAddressChanged)
    def hue_bridge_address(self):
        return self._hue_bridge_address_value

    @hue_bridge_address.setter
    def hue_bridge_address(self, value):
        if self._hue_bridge_address_value != value:
            self._hue_bridge_address_value = value
            self.hueBridgeAddressChanged.emit(value)

    # Hue Bridge Username
    @Property(str, notify=hueBridgeUsernameChanged)
    def hue_bridge_username(self):
        return self._hue_bridge_username_value

    @hue_bridge_username.setter
    def hue_bridge_username(self, value):
        if self._hue_bridge_username_value != value:
            self._hue_bridge_username_value = value
            self.hueBridgeUsernameChanged.emit(value)

    # Hue Bridge Clientkey
    @Property(str, notify=hueBridgeClientkeyChanged)
    def hue_bridge_clientkey(self):
        return self._hue_bridge_clientkey_value

    @hue_bridge_clientkey.setter
    def hue_bridge_clientkey(self, value):
        if self._hue_bridge_clientkey_value != value:
            self._hue_bridge_clientkey_value = value
            self.hueBridgeClientkeyChanged.emit(value)

    # Hue Min Brightness
    @Property(int, notify=hueMinBrightnessChanged)
    def hue_min_brightness(self):
        return self._hue_min_brightness_value

    @hue_min_brightness.setter
    def hue_min_brightness(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Hue min brightness must be a number")
        value = int(value)
        if self._hue_min_brightness_value != value:
            self._hue_min_brightness_value = value
            self.hueMinBrightnessChanged.emit(value)

    # Hue Max Brightness
    @Property(int, notify=hueMaxBrightnessChanged)
    def hue_max_brightness(self):
        return self._hue_max_brightness_value

    @hue_max_brightness.setter
    def hue_max_brightness(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Hue max brightness must be a number")
        value = int(value)
        if self._hue_max_brightness_value != value:
            self._hue_max_brightness_value = value
            self.hueMaxBrightnessChanged.emit(value)

    # Hue Color Saturation
    @Property(int, notify=hueSaturationChanged)
    def hue_saturation(self):
        return self._hue_saturation_value

    @hue_saturation.setter
    def hue_saturation(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Hue max brightness must be a number")
        value = float(value)
        if self._hue_saturation_value != value:
            self._hue_saturation_value = value
            self.hueSaturationChanged.emit(value)

    def save(self):
        """
        Saves the current configuration to a JSON file.
        """
        data = {
            'blur_factor': self._blur_factor_value,
            'brightness': self._brightness_value,
            'hue_bridge_address': self._hue_bridge_address_value,
            'hue_bridge_username': self._hue_bridge_username_value,
            'hue_bridge_clientkey': self._hue_bridge_clientkey_value,
            'hue_min_brightness': self._hue_min_brightness_value,
            'hue_max_brightness': self._hue_max_brightness_value,
            'hue_saturation': self._hue_saturation_value
        }
        with open(self._filename, "w") as json_file:
            json.dump(data, json_file)

    def load(self):
        """
        Loads the previously saved configuration from a JSON file.
        """
        with open(self._filename, "r") as json_file:
            data = json.load(json_file)
            
        # Use property setters to ensure signals are emitted
        self.blur_factor = data['blur_factor']
        self.brightness = data.get('brightness', 50)
        self.hue_bridge_address = data.get('hue_bridge_address', '')
        self.hue_bridge_username = data.get('hue_bridge_username', '')
        self.hue_bridge_clientkey = data.get('hue_bridge_clientkey', '')
        self.hue_min_brightness = data.get('hue_min_brightness', 1)
        self.hue_max_brightness = data.get('hue_max_brightness', 254)
        self.hue_saturation = data.get('hue_saturation', 1.0)
