import os
import json

from appdirs import user_data_dir


class ConfigValues:
    def __init__(self):
        self._blur_factor_value = 50
        self._num_windows_value = 3
        self._brightness_value = 50  # Add default brightness value
        self._hue_bridge_address_value = ''
        self._hue_bridge_username_value = ''
        self._hue_min_brightness_value = 1
        self._hue_max_brightness_value = 254

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

    @property
    def blur_factor(self):
        return self._blur_factor_value

    @blur_factor.setter
    def blur_factor(self, value):
        if not isinstance(value, int):
            raise TypeError("Blur factor must be an integer")
        elif not 0 <= value <= 100:
            raise ValueError("Blur factor out of range (0-100)")

        self._blur_factor_value = value

    @property
    def num_windows(self):
        return self._num_windows_value

    @num_windows.setter
    def num_windows(self, value):
        if not isinstance(value, int):
            raise TypeError("Number of windows must be an integer")
        elif not 0 <= value <= 6:
            raise ValueError("Number of windows out of range (0-6)")

        self._num_windows_value = value

    @property
    def brightness(self):
        return self._brightness_value

    @brightness.setter
    def brightness(self, value):
        if not isinstance(value, int):
            raise TypeError("Brightness must be an integer")
        elif not 0 <= value <= 100:
            raise ValueError("Brightness out of range (0-100)")

        self._brightness_value = value

    @property
    def hue_bridge_address(self):
        return self._hue_bridge_address_value

    @hue_bridge_address.setter
    def hue_bridge_address(self, value):
        self._hue_bridge_address_value = value

    @property
    def hue_bridge_username(self):
        return self._hue_bridge_username_value

    @hue_bridge_username.setter
    def hue_bridge_username(self, value):
        self._hue_bridge_username_value = value

    @property
    def hue_min_brightness(self):
        return self._hue_min_brightness_value

    @hue_min_brightness.setter
    def hue_min_brightness(self, value):
        self._hue_min_brightness_value = value

    @property
    def hue_max_brightness(self):
        return self._hue_max_brightness_value

    @hue_max_brightness.setter
    def hue_max_brightness(self, value):
        self._hue_max_brightness_value = value

    def save(self):
        """
        Saves the current configuration to a JSON file.
        """
        data = {
            'blur_factor': self._blur_factor_value,
            'num_windows': self._num_windows_value,
            'brightness': self._brightness_value,
            'hue_bridge_address': self._hue_bridge_address_value,
            'hue_bridge_username': self._hue_bridge_username_value,
            'hue_min_brightness': self._hue_min_brightness_value,
            'hue_max_brightness': self._hue_max_brightness_value
        }
        with open(self._filename, "w") as json_file:
            json.dump(data, json_file)
    def load(self):
        """
        Loads the previously saved configuration from a JSON file.
        """
        with open(self._filename, "r") as json_file:
            data = json.load(json_file)
        self._blur_factor_value = data['blur_factor']
        self._num_windows_value = data['num_windows']
        self._brightness_value = data.get('brightness', 50)
        self._hue_bridge_address_value = data.get('hue_bridge_address', '')
        self._hue_bridge_username_value = data.get('hue_bridge_username', '')
        self._hue_min_brightness_value = data.get('hue_min_brightness', 1)
        self._hue_max_brightness_value = data.get('hue_max_brightness', 254)
