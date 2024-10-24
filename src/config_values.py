import os
import json

from appdirs import user_data_dir


class ConfigValues:
    def __init__(self):
        self._blur_factor_value = 50
        self._num_windows_value = 3

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

    def save(self):
        """
        Saves the current configuration to a JSON file.
        """
        with open(self._filename, "w") as json_file:
            json.dump({"blur_factor": self._blur_factor_value, "num_windows": self._num_windows_value}, json_file)

    def load(self):
        """
        Loads the previously saved configuration from a JSON file.
        """
        with open(self._filename, "r") as json_file:
            data = json.load(json_file)
        self._blur_factor_value = data['blur_factor']
        self._num_windows_value = data['num_windows']