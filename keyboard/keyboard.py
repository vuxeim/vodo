import threading

from keyboard import getkey
import keyboard


class _Cursor:

    @staticmethod
    def hide():
        print('\x1b[?25l', end='')

    @staticmethod
    def show():
        print('\x1b[?25h', end='')


class Keyboard(threading.Thread):

    def __init__(self):
        super().__init__()
        self.cursor: type[_Cursor] = _Cursor
        self.echo: bool = True
        self._buffer: str = ""
        self.capture: bool = False
        self._pressed: dict[str, bool] = {}
        self._running: bool = True
        self.daemon: bool = True
        self.start()

    def run(self) -> None:
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
        val: bool = self._pressed.setdefault(key, False)
        if once:
            self._pressed[key] = False
        return val

    def accumulate(self) -> None:
        self.capture = True
        self.echo = True
        self.cursor.show()

    def collect(self, delimeter: str = keyboard.key.ENTER) -> str | None:
        if not self._buffer.endswith(delimeter):
            return None
        self.echo = False
        self.cursor.hide()
        buf = self._buffer
        self._buffer = ""
        self.capture = False
        return buf

    def stop(self) -> None:
        """ Safely kills the keyboard thread """
        self._running = False
        self.cursor.show()
