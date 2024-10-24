
import re
import signal
import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

from config_values import ConfigValues

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

class AmbianceWindow:
    def __init__(self, config_values):
        self._config = config_values

        DBusGMainLoop(set_as_default=True)
        Gst.init(None)

        self.loop = GLib.MainLoop()

        self.bus = dbus.SessionBus()
        self.request_iface = 'org.freedesktop.portal.Request'
        self.screen_cast_iface = 'org.freedesktop.portal.ScreenCast'

        self.pipeline = None

        self.request_token_counter = 0
        self.session_token_counter = 0
        
    def run(self):
        self.sender_name = re.sub(r'\.', r'_', self.bus.get_unique_name()[1:])

        self.portal = self.bus.get_object('org.freedesktop.portal.Desktop',
                                    '/org/freedesktop/portal/desktop')

        (self.session_path, self.session_token) = self.new_session_path()

        self.screen_cast_call(self.portal.CreateSession, self.on_create_session_response,
                        options={ 'session_handle_token': self.session_token })

        try:
            self.loop.run()
        except KeyboardInterrupt:
            self.terminate()

    def terminate(self):
        if self.pipeline is not None:
            self.pipeline.set_state(Gst.State.NULL)
        self.loop.quit()

    def new_request_path(self):
        self.request_token_counter = self.request_token_counter + 1
        token = 'u%d'%self.request_token_counter
        path = '/org/freedesktop/portal/desktop/request/%s/%s'%(self.sender_name, token)
        return (path, token)

    def new_session_path(self):
        self.session_token_counter = self.session_token_counter + 1
        token = 'u%d'%self.session_token_counter
        path = '/org/freedesktop/portal/desktop/session/%s/%s'%(self.sender_name, token)
        return (path, token)

    def screen_cast_call(self, method, callback, *args, options={}):
        (request_path, request_token) = self.new_request_path()
        self.bus.add_signal_receiver(callback,
                                'Response',
                                self.request_iface,
                                'org.freedesktop.portal.Desktop',
                                request_path)
        options['handle_token'] = request_token
        method(*(args + (options, )),
            dbus_interface=self.screen_cast_iface)

    def on_gst_message(self, bus, message):
        type = message.type
        if type == Gst.MessageType.EOS or type == Gst.MessageType.ERROR:
            self.terminate()

    def play_pipewire_stream(self, node_id):
        with open('myshader.frag', 'r') as shaderfile:
            shadercode = shaderfile.read()

        empty_dict = dbus.Dictionary(signature="sv")
        fd_object = self.portal.OpenPipeWireRemote(self.session, empty_dict,
                                            dbus_interface=self.screen_cast_iface)
        fd = fd_object.take()
        blur = f'glupload ! gltransformation scale-x=0.02 scale-y=0.02 rotation-y=180 ! gleffects effect=blur hswap=1 ! glshader fragment="{shadercode}" ! gltransformation scale-x=50.0 scale-y=50.0 ! gldownload'
        vc= 'videoconvert'
        #capture=f'pipewiresrc fd={fd} path={node_id} ! {vc} ! videorate ! video/x-raw,framerate=10/1'
        capture=f'pipewiresrc fd={fd} path={node_id} ! {vc} '
        display=f'{vc} ! xvimagesink force-aspect-ratio=false'
        pipecmd = f'''{capture} ! {blur} ! {vc} ! tee name=m
        m. ! queue ! {display}
        m. ! queue ! {display}
        '''
        self.pipeline = Gst.parse_launch(pipecmd)
        self.pipeline.set_state(Gst.State.PLAYING)
        self.pipeline.get_bus().connect('message', self.on_gst_message)

    def on_start_response(self, response, results):
        if response != 0:
            print("Failed to start: %s"%response)
            self.terminate()
            return

        print("streams:")
        for (node_id, stream_properties) in results['streams']:
            print("stream {}".format(node_id))
            self.play_pipewire_stream(node_id)

    def on_select_sources_response(self, response, results):
        if response != 0:
            print("Failed to select sources: %d"%response)
            self.terminate()
            return

        print("sources selected")
        self.screen_cast_call(self.portal.Start, self.on_start_response,
                        self.session, '')

    def on_create_session_response(self, response, results):
        if response != 0:
            print("Failed to create session: %d"%response)
            self.terminate()
            return

        self.session = results['session_handle']
        print("session %s created"%self.session)

        self.screen_cast_call(self.portal.SelectSources, self.on_select_sources_response,
                        self.session,
                        options={ 'multiple': False,
                                'types': dbus.UInt32(1|2) })
