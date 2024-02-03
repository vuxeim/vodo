from __future__ import annotations
from typing import Self

try:
    from ctypes import (WinDLL, WinError,
        LibraryLoader, byref, wintypes)
except ImportError:
    # Not running on Windows
    WinDLL = None

def _WindowsInit():
    windll = LibraryLoader(WinDLL)
    _GetStdHandle = windll.kernel32.GetStdHandle
    _GetConsoleMode = windll.kernel32.GetConsoleMode
    _SetConsoleMode = windll.kernel32.SetConsoleMode
    handle = _GetStdHandle(-11)
    if handle == -1:
        raise WinError()
    mode = wintypes.DWORD()
    success = _GetConsoleMode(handle, byref(mode))
    if not success:
        raise WinError()
    success = _SetConsoleMode(handle, mode.value|4)
    if not success:
        raise WinError()
if WinDLL is not None:
    _WindowsInit()

_names: dict[int, str] = {
    0: 'style',
    3: 'fore', 9: 'fore',
    4: 'back', 10: 'back',
}

# https://en.wikipedia.org/wiki/ANSI_escape_code

class BUFFER:
    ALTERNATIVE = '\x1b[?1049h'
    ALT = ALTERNATIVE
    NORMAL = '\x1b[?1049l'

class CURSOR:
    BACK = '\x1b[%dD'
    FORWARD = '\x1b[%dC'
    UP = '\x1b[%dA'
    DOWN = '\x1b[%dB'
    def __new__(cls, x: int = 0, y: int = 0) -> str:
        return f'\x1b[{x};{y}H'

class STYLE:
    RESET = 0
    NONE = 0
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    SLOW_BLINK = 5
    FAST_BLINK = 6
    INVERT = 7
    REVERSE = 7
    HIDE = 8
    STRIKE = 9
    DOUBLE_UNDERLINE = 21
    DUNDER = 21

class FORE:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    class LIGHT:
        BLACK = 90
        RED = 91
        GREEN = 92
        YELLOW = 93
        BLUE = 94
        MAGENTA = 95
        CYAN = 96
        WHITE = 97

    BRIGHT = LIGHT

class BACK:
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47

    class LIGHT:
        BLACK = 100
        RED = 101
        GREEN = 102
        YELLOW = 103
        BLUE = 104
        MAGENTA = 105
        CYAN = 106
        WHITE = 107

    BRIGHT = LIGHT

class Palette:

    RESET = '\x1b[0m'

    def __init__(self, *styles: int, fmt: str = "{}") -> None:
        self._format = fmt
        self._list: list[int] = sorted(styles)
        self._style: str = str()
        self.compile()

    def compile(self) -> None:
        self._style = '\x1b[' + ';'.join(str(s) for s in self._list) + 'm'

    @property
    def _codes(self) -> dict[str, int]:
        return {__class__._get_type(code): code for code in self._list}

    @staticmethod
    def _get_type(code: int) -> str:
        prefix = (code - code%10) // 10
        return _names.get(prefix, 'none')

    def combine(self, *other: int) -> list[int]:
        combined = self._codes | {__class__._get_type(code): code for code in other}
        return sorted(combined.values())

    def print(self, text: str) -> None:
        print(self(text))

    def __call__(self, text: str) -> str:
        return self._style + self._format.format(text) + __class__.RESET

    def __ixor__(self, other: int) -> Self:
        if other in self._list:
            self._list.remove(other)
        else:
            self._list.append(other)
        self.compile()
        return self

    def __iadd__(self, other: int) -> Self:
        self._list = self.combine(other)
        self.compile()
        return self

    def __add__(self, other: int) -> Palette:
        _list = self.combine(other)
        return self.__class__(*_list)

    def __or__(self, other: Palette) -> Palette:
        _list = self.combine(*other._list)
        return self.__class__(*_list)

    def __len__(self) -> int:
        return len(self._list)

class Color:
    pass

for color in dir(FORE):
    if color.isupper() and color not in ('LIGHT', 'BRIGHT'):
        light = 'LIGHT'+color
        setattr(Color, color.lower(), Palette(getattr(FORE, color)))
        setattr(Color, light.lower(), Palette(getattr(FORE.LIGHT, color)))

