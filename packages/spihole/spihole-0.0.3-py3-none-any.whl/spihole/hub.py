import enum
import queue
import threading
from abc import ABCMeta
from typing import Any


class HubSubscriber(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'on_message') and callable(subclass.on_message) or NotImplemented


class HubMessageType(enum.Enum):
    DATA = 1
    EVENT = 2


class HubMessage():
    def __init__(self, msg_type: HubMessageType, content: Any) -> None:
        super().__init__()
        self.type: HubMessageType = msg_type
        self.content: Any = content


class Hub(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self._subscribers = set()
        self._bus = queue.Queue()
        self._stop_evt = threading.Event()

    def add_subscriber(self, subscriber: HubSubscriber):
        if not isinstance(subscriber, HubSubscriber):
            raise ValueError('Bad interface')
        self._subscribers.add(subscriber)

    def run(self) -> None:
        while not self._stop_evt.is_set():
            try:
                data = self._bus.get(5)
                self._distribute(data)
            except queue.Empty:
                pass
        self._stop_evt.clear()

    def stop(self) -> None:
        self._stop_evt.set()
        self.join()

    def _distribute(self, message: HubMessage) -> None:
        subscriber: HubSubscriber
        for subscriber in self._subscribers:
            subscriber.on_message(message)

    @property
    def bus(self):
        return self._bus
