try:
    import picamera
except ImportError:
    import fake_rpi.picamera as picamera

import io
import logging
import threading
import time

from .hub import Hub
from .hub import HubMessage
from .hub import HubMessageType
from .keypad import KeyTypes


class Capture(threading.Thread):
    def __init__(self, hub: Hub) -> None:
        super().__init__()
        self.daemon = True
        self.camera: picamera.PiCamera
        self._stop_evt = threading.Event()
        self._data_queue = hub.bus
        hub.add_subscriber(self)
        self._message = HubMessage(HubMessageType.DATA, bytes())
        self._zoom_factor = 0
        self._events = {
            KeyTypes.KEY1: lambda: None,  # Turn on capture
            KeyTypes.KEY2: lambda: None,  # Mirror image
            KeyTypes.KEY3: lambda: None,  # TBD
            KeyTypes.UP: lambda: self._zoom(0.1),    # camera zoom in
            KeyTypes.DOWN: lambda: self._zoom(-0.1),  # camera zoom out
            KeyTypes.LEFT: lambda: self._rotate(-90),  # Rotate left
            KeyTypes.RIGHT: lambda: self._rotate(90),  # Rotate right
            KeyTypes.PRESS: lambda: self._reset()  # Reset settings
        }

    def run(self) -> None:
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1920, 1080)
        self.camera.framerate = 30
        time.sleep(2)  # camera initialization
        stream = io.BytesIO()
        for _ in self.camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            try:
                stream.seek(0)
                self._message.content = stream.read()
                self._data_queue.put_nowait(self._message)
            except Exception:
                pass
            finally:
                stream.seek(0)
                stream.truncate()
            if self._stop_evt.is_set():
                break
        self.camera.close()
        self._stop_evt.clear()

    def stop(self) -> None:
        self._stop_evt.set()

    def on_message(self, message: HubMessage):
        if message.type == HubMessageType.EVENT:
            event_type = message.content
            logging.debug('Event received: %r', event_type)
            self._events.get(event_type, lambda: None)()

    def _rotate(self, inc):
        self.camera.rotation = self.camera.rotation + inc

    def _zoom(self, inc):
        zf = self._zoom_factor
        zf += inc
        if zf > 0.4:
            zf = 0.4
        if zf < 0:
            zf = 0
        if zf == self._zoom_factor:
            return
        self._zoom_factor = zf
        logging.debug('Setting zoom factor to: %f', zf)
        self.camera.zoom = (0+zf, 0+zf, 1-2*zf, 1-2*zf)

    def _reset(self):
        self._zoom_factor = 0
        self.camera.zoom = (0, 0, 1, 1)
        self.camera.rotation = 0
