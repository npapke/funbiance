
import re
import signal
import dbus
import math
from dbus.mainloop.glib import DBusGMainLoop
import numpy as np
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtGui import QImage, QPixmap
import cv2


from config_values import ConfigValues

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

class CapturePipeline(QObject):
    
    color_sample = Signal(int, int, int)        # RGB
    frame_sample = Signal(QPixmap)
    
    def __init__(self, config_values):
        super().__init__()
        self._config = config_values

        DBusGMainLoop(set_as_default=True)
        Gst.init(None)

        self.bus = dbus.SessionBus()
        self.request_iface = 'org.freedesktop.portal.Request'
        self.screen_cast_iface = 'org.freedesktop.portal.ScreenCast'
        self.session_iface = 'org.freedesktop.portal.Session'

        self.portal = self.bus.get_object('org.freedesktop.portal.Desktop',
                                    '/org/freedesktop/portal/desktop')

        self.pipeline = None

        self.request_token_counter = 0
        self.session_token_counter = 0
        
        self._pixmap = None
        
        
    def run(self):
        if self.pipeline is not None:
            return
        
        self.sender_name = re.sub(r'\.', r'_', self.bus.get_unique_name()[1:])

        (self.session_path, self.session_token) = self.new_session_path()

        self.screen_cast_call(self.portal.CreateSession, self.on_create_session_response,
                        options={ 'session_handle_token': self.session_token })

    def terminate(self):
        if self.pipeline is not None:
            self.pipeline.set_state(Gst.State.NULL)
            self.pipeline = None

        # TODO Find a way to close the session.  The following does not work.
        # if hasattr(self, 'session') and self.session:
            # self.portal.Close(dbus_interface=self.session_iface)
            # self.screen_cast_call(self.portal.Close, self.on_close_session_response)

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
        empty_dict = dbus.Dictionary(signature="sv")
        fd_object = self.portal.OpenPipeWireRemote(self.session, empty_dict,
                                            dbus_interface=self.screen_cast_iface)
        fd = fd_object.take()
        
        pipecmd = (
                f'pipewiresrc fd={fd} path={node_id} ! '
                'videoconvert ! ' 
                'video/x-raw,format=RGB ! ' 
                'appsink name=frame_sink emit-signals=True sync=False'
            )
        # display=f'{vc} ! xvimagesink force-aspect-ratio=false'
        self.pipeline = Gst.parse_launch(pipecmd)
        appsink = self.pipeline.get_by_name('frame_sink')
        appsink.connect("new-sample", self.on_buffer, None)
        self.pipeline.set_state(Gst.State.PLAYING)
        self.pipeline.get_bus().connect('message', self.on_gst_message)
        
        
    def on_buffer(self, sink, data):
        sample = sink.emit("pull-sample")
        try:
            if sample:
                buffer = sample.get_buffer()
                caps = sample.get_caps()
                
                # Get buffer dimensions
                width = caps.get_structure(0).get_value('width')
                height = caps.get_structure(0).get_value('height')
                
                # Create numpy array from buffer data
                buffer_data = buffer.extract_dup(0, buffer.get_size())
                numpy_frame = np.ndarray(
                    (height, width, 3),
                    buffer=buffer_data,
                    dtype=np.uint8
                )
                
                # Calculate average RGB values across all pixels
                r = int(np.mean(numpy_frame[:,:,0]))
                g = int(np.mean(numpy_frame[:,:,1])) 
                b = int(np.mean(numpy_frame[:,:,2]))
                self.color_sample.emit(r, g, b)
                # print(f"r={r} g={g} b={b}")
                
                # Once we have the mean color, let's perform some transformations.
                scale_down = (1.0 - math.log(self._config.blur_factor + 1, 100)) if self._config.blur_factor < 99 else 0.001
                width = int(width * scale_down)
                height = int(height * scale_down)

                numpy_frame = cv2.resize(numpy_frame, (width, height), interpolation = cv2.INTER_AREA)
                numpy_frame = np.clip(numpy_frame * (self._config.brightness / 100.0), 0, 255).astype(np.uint8)
                numpy_frame = cv2.GaussianBlur(numpy_frame, (15, 15), 8)
                numpy_frame = cv2.flip(numpy_frame, 1)
                
                # Convert numpy array to QImage
                height, width, channels = numpy_frame.shape
                bytes_per_line = channels * width
                qimage = QImage(
                    numpy_frame.data,
                    width,
                    height, 
                    bytes_per_line,
                    QImage.Format_RGB888
                )
                
                self._pixmap = QPixmap.fromImage(qimage)
                self.frame_sample.emit(self._pixmap)
                
                return Gst.FlowReturn.OK
        except Exception as e:
            print(f"capture_pipeline: exception {e}")
        
        return Gst.FlowReturn.ERROR
    
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
        
    def on_close_session_response(self, response):
        if response != 0:
            print("Failed to close session %s"%self.session)
            
            
    def shader_code(self):
        brightness = self._config.brightness / 100
        return f"""
#version 100
#ifdef GL_ES
precision mediump float;
#endif
varying vec2 v_texcoord;
uniform sampler2D tex;
uniform float time;
uniform float width;
uniform float height;

void main () {{
	gl_FragColor = texture2D( tex, v_texcoord ) * vec4({brightness}, {brightness}, {brightness}, {brightness});
}}
    """
