import threading

from . import getkey
from .code import key

class Keyboard(threading.Thread):

    def __init__(self):
        super().__init__()
        self._buffer: str = ""
        self.capture: bool = False
        self._pressed: dict[str, bool] = {}
        self._running: bool = True
        self.daemon: bool = True
        self.start()

    def run(self) -> None:
        with getkey.context():
            while self._running:
                key = getkey.getkey()
                if self.capture:
                    self._buffer += key
                else:
                    self._set_pressed(key)

    def clear(self) -> None:
        self._pressed.clear()

    def _set_pressed(self, key) -> None:
        self._pressed[key] = True

    def is_pressed(self, key: str, once=True) -> bool:
        if self.capture:
            return False
        val = self._pressed.setdefault(key, False)
        if once:
            self._pressed[key] = False
        return val

    def input_mode(self) -> None:
        self.capture = True

    def fetch(self) -> str:
        buf = self._buffer
        self._buffer = ""
        return buf

    def normal_mode(self) -> None:
        self.capture = False
        self._buffer = ""

    def stop(self) -> None:
        """ Safely kills the keyboard thread """
        self._running = False

