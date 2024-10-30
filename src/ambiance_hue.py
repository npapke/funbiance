from PySide6.QtCore import Slot, QObject
import rgbxy
import time
import socket
import json
import requests
import urllib3
from hue_entertainment_pykit import create_bridge, Entertainment, Streaming, Bridge

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
        
        bridge_params = self.make_bridge_params(config_values.hue_bridge_address, config_values.hue_bridge_username, config_values.hue_bridge_clientkey)
        self.bridge: Bridge = create_bridge(**bridge_params)

        # Set up the Entertainment API service
        entertainment_service = Entertainment(self.bridge)

        # Fetch all Entertainment Configurations on the Hue bridge
        entertainment_configs = entertainment_service.get_entertainment_configs()
        for id in entertainment_configs:
            print(f"Entertainment configurations: {id} = {entertainment_configs[id].name}")
            for channel in entertainment_configs[id].channels:
                print(f"\tchannel: {channel.channel_id} position={channel.position}")

        # TODO: Add some Entertainment Area selection logic
        # For the purposes of example I'm going to do manual selection
        self.entertainment_config = list(entertainment_configs.values())[1]

        # Set up the Streaming service
        self.streaming = Streaming(
            self.bridge, self.entertainment_config, entertainment_service.get_ent_conf_repo()
        )

        # Start streaming messages to the bridge
        self.streaming.start_stream()

        # Set the color space to xyb or rgb
        self.streaming.set_color_space("xyb")


        self.last_update_time = 0
        
        # Recommendation is 60 Hz
        self.min_update_interval = 1/60
        
    def __del__(self):
        if self.streaming:
            self.streaming.stop_stream()
        super().__del__()
    

    def make_bridge_params(self, bridge_address: str, bridge_username: str, bridge_clientkey: str) -> dict[str, str]:
        if not bridge_username or not bridge_clientkey:
            # TODO Bridge enrollment
            raise Exception("Missing bridge username or clientkey")
        
        bridge_params: dict[str, str] = {
            "username": bridge_username,
            "clientkey": bridge_clientkey
        }

        # hue_entertainment_pykit wants an IP address not a hostname
        try:
            bridge_params["ip_address"] = socket.gethostbyname(bridge_address)
        except:
            # Perhaps we already have an IP address?
            bridge_params["ip_address"] = bridge_address

        # Define the URL and headers
        headers: dict[str, str] = {
            "hue-application-key": bridge_username
        }

        # Hue Bridges have self-signed certs
        urllib3.disable_warnings()
        
        # The "bridge" resource has some of the necessary information.
        response: requests.Response = requests.get(f"https://{bridge_address}/clip/v2/resource/bridge", headers=headers, verify=False)

        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            print(data)
            
            bridge_params["identification"] = data["data"][0]["id"]
            bridge_params["rid"] = data["data"][0]["owner"]["rid"]
            
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            
        response: requests.Response = requests.get(f"https://{bridge_address}/api/config", headers=headers, verify=False)

        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            print(data)
            
            bridge_params["swversion"] = int(data["swversion"])
            bridge_params["name"] = data["name"]
            
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            
            
        response: requests.Response = requests.get(f"https://{bridge_address}/auth/v1", headers=headers, verify=False)

        # Check if request was successful
        if response.status_code == 200:
            print(response.headers)
            bridge_params["hue_app_id"] = response.headers["hue-application-id"]
            
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            
        print("Bridge params:", json.dumps(bridge_params, indent=4))
        return bridge_params

    @Slot(int, int, int)
    def set_color(self, r: int, g: int, b: int) -> None:
        current_time = time.time()
        if current_time - self.last_update_time < self.min_update_interval:
            return
        self.last_update_time = current_time

        color = (r, g, b)
        xy = self.rgb_to_xy(color)
        
        min_brightness = max(self.HUE_MIN_BRIGHTNESS, self._config.hue_min_brightness) / 255.0
        max_brightness = min(self.HUE_MAX_BRIGHTNESS, self._config.hue_max_brightness) / 255.0
        bri = min(max(self.get_luminance(color), min_brightness), max_brightness)

        for channel in range(len(self.entertainment_config.channels)):
            input = (*xy, bri, channel)
            self.streaming.set_input(input)

    def rgb_to_xy(self, color):
        # Prevent DivisionByZero exception in rgbxy library:
        # https://github.com/benknight/hue-python-rgb-converter/issues/6
        color = tuple(max(component, 10 ** -3) for component in color)
        return self._color_converter.rgb_to_xy(*color)

    def get_luminance(self, color):
        return sum(x * y for x, y in zip(color, self.LUMINANCE_MULTIPLIERS)) / 255.0