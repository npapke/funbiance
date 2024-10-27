import atexit
from PySide6.QtCore import Slot, QObject
import qhue
import rgbxy
import time

from config_values import ConfigValues


class AmbianceHue(QObject):
    
    HUE_MIN_BRIGHTNESS = 1
    HUE_MAX_BRIGHTNESS = 254
    NON_MODIFIABLE_STATES = ['colormode', 'reachable', 'mode']
    
    # https://en.wikipedia.org/wiki/Relative_luminance
    LUMINANCE_MULTIPLIERS = (0.2126, 0.7152, 0.0722)
    
    def __init__(self, config_values: ConfigValues) -> None:
        super().__init__()
        self._color_converter = rgbxy.Converter()
        self._config = config_values
        username = config_values.hue_bridge_username
        if not username:
            username = self.prompt_create_username(config_values.hue_bridge_address)
            if not username:
                raise RuntimeError('Cannot get authentication info for bridge')
            config_values.hue_bridge_username = username

        self.bridge = qhue.Bridge(config_values.hue_bridge_address, username)
        self.previous_color = None
        
        # TODO Hack
        self._config.lights = [19, 20]

        self.initial_states = {}
        for light in config_values.lights:
            state = self.bridge.lights[light]()['state']
            self.initial_states[light] = state
            self.bridge.lights[light].state(on=True)

        def restore_state():
            for light, state in self.initial_states.items():
                self.change_light_state(self.bridge, light, state)

        atexit.register(restore_state)

        self.min_brightness = max(self.HUE_MIN_BRIGHTNESS,
                                  int(round(self._config.hue_min_brightness / 100 * self.HUE_MAX_BRIGHTNESS)))
        self.max_brightness = min(self.HUE_MAX_BRIGHTNESS,
                                  int(round(self._config.hue_max_brightness / 100 * self.HUE_MAX_BRIGHTNESS)))
        self.last_update_time = 0
        self.min_update_interval = 1/5  # frames per second
    

    @Slot(int, int, int)
    def set_color(self, r: int, g: int, b: int) -> None:
        current_time = time.time()
        if current_time - self.last_update_time < self.min_update_interval:
            return
        self.last_update_time = current_time

        color = (r, g, b)
        if color != self.previous_color:
            state = {
                'xy': self.rgb_to_xy(color),
                'bri' : max(self.min_brightness, int(round(self.get_relative_luminance(color * self.max_brightness))))
            }

            for light in self._config.lights:
                self.change_light_state(light, state)
            self.previous_color = color

    def prompt_create_username(self, bridge_address: str) -> str:
        choice = input('No username specified, do you want to create one now? [Y/n]: ')
        if choice.lower() in {'', 'y', 'yes'}:
            try:
                return qhue.create_new_username(bridge_address)
            except qhue.QhueException as exception:
                print(f'Exception occurred while creating the username: {exception}')
        return None

    def change_light_state(self, light, state):
        for key in self.NON_MODIFIABLE_STATES:
            if key in state:
                del state[key]

        try:
            print(f'Setting {light} to {state}')
            self.bridge.lights[light].state(**state)
        except Exception:
            pass

    def rgb_to_xy(self, color):
        # Prevent DivisionByZero exception in rgbxy library:
        # https://github.com/benknight/hue-python-rgb-converter/issues/6
        color = tuple(max(component, 10 ** -3) for component in color)
        return self._color_converter.rgb_to_xy(*color)

    def get_relative_luminance(self, color):
        return sum(x * y for x, y in zip(color, self.LUMINANCE_MULTIPLIERS)) / \
            sum(x * y for x, y in zip((255, 255, 255), self.LUMINANCE_MULTIPLIERS))