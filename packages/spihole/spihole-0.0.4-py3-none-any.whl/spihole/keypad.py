import enum
import threading

try:
    import RPi.GPIO as GPIO
except ImportError:
    from fake_rpi.RPi import GPIO


from .hub import Hub
from .hub import HubMessage
from .hub import HubMessageType


class KeyTypes(enum.IntEnum):
    LEFT = 5
    UP = 6
    PRESS = 13
    DOWN = 19
    RIGHT = 26
    KEY1 = 21
    KEY2 = 20
    KEY3 = 16


class KeyPad(threading.Thread):
    def __init__(self, hub: Hub) -> None:
        super().__init__()
        self._stop_evt = threading.Event()
        self._message_bus = hub.bus
        self._message = HubMessage(HubMessageType.EVENT, None)

    def run(self) -> None:
        self._gpio_setup()
        while not self._stop_evt.is_set():
            self._stop_evt.wait(30)
        self._stop_evt.clear()
        self._cleanup()

    def stop(self) -> None:
        self._stop_evt.set()

    def _gpio_setup(self):
        GPIO.setmode(GPIO.BCM)
        for key in KeyTypes:
            GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(key, GPIO.FALLING, callback=self._on_key_pressed, bouncetime=200)

    def _on_key_pressed(self, key):
        key_type = KeyTypes(key)
        self._message.content = key_type
        self._message_bus.put_nowait(self._message)

    def _cleanup(self):
        for key in KeyTypes:
            GPIO.remove_event_detect(key)
