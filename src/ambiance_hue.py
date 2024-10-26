import atexit
from PySide6.QtCore import Slot, QObject
import qhue
from qhue import QhueException

from amby.config import get_saved_username, save_username
from amby.constants import NON_MODIFIABLE_STATES, PHILIPS_MAX_BRIGHTNESS, PHILIPS_MIN_BRIGHTNESS
from amby.core import get_relative_luminance, rgb_to_xy


class AmbianceHue(QObject):

    def __init__(self, arguments):
        super().__init__()
        self.arguments = arguments
        self.username = arguments.username or get_saved_username()
        if not self.username:
            self.username = self.prompt_create_username(arguments.bridge_address)
            if not self.username:
                raise RuntimeError('Cannot get authentication info for bridge')
            save_username(self.username)

        self.bridge = qhue.Bridge(arguments.bridge_address, self.username)
        self.previous_color = None

        self.initial_states = {}
        for light in arguments.lights:
            state = self.bridge.lights[light]()['state']
            self.initial_states[light] = state
            if arguments.enable and not state['on']:
                self.bridge.lights[light].state(on=True)

        if arguments.restore_state:
            def restore_state():
                for light, state in self.initial_states.items():
                    self.change_light_state(self.bridge, light, state)

            atexit.register(restore_state)

        self.min_brightness = max(PHILIPS_MIN_BRIGHTNESS,
                                  int(round(self.arguments.min_brightness / 100 * PHILIPS_MAX_BRIGHTNESS)))
        self.max_brightness = min(PHILIPS_MAX_BRIGHTNESS,
                                  int(round(self.arguments.max_brightness / 100 * PHILIPS_MAX_BRIGHTNESS)))

    @Slot(list)
    def set_color(self, colors):
        if colors[0] != self.previous_color:
            state = {'xy': rgb_to_xy(colors[0])}
            if self.arguments.change_brightness:
                state['bri'] = max(self.min_brightness, int(round(get_relative_luminance(colors[0]) * self.max_brightness)))

            for light in self.arguments.lights:
                self.change_light_state(self.bridge, light, state)
            self.previous_color = colors[0]

    @staticmethod
    def prompt_create_username(bridge_address):
        choice = input('No username specified, do you want to create one now? [Y/n]: ')
        if choice.lower() in {'', 'y', 'yes'}:
            try:
                return qhue.create_new_username(bridge_address)
            except QhueException as exception:
                print(f'Exception occurred while creating the username: {exception}')

    @staticmethod
    def change_light_state(bridge, light, state):
        for key in NON_MODIFIABLE_STATES:
            if key in state:
                del state[key]

        try:
            bridge.lights[light].state(**state)
        except Exception:
            pass
