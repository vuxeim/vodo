from __future__ import annotations
from typing import Self

# https://en.wikipedia.org/wiki/ANSI_escape_code
class InvalidCode(Exception):
    pass

_names: dict[int, str] = {
    0: 'style',
    3: 'fore', 9: 'fore',
    4: 'back', 10: 'back',
}

class BUFFER:

    ALTERNATIVE = '\x1b[?1049h'
    ALT = ALTERNATIVE
    NORMAL = '\x1b[?1049l'

class CURSOR:

    BACK = '\x1b[%dD'
    FORWARD = '\x1b[%dC'
    UP = '\x1b[%dA'
    DOWN = '\x1b[%dB'

    def __new__(cls, x: int = 1, y: int = 1) -> str:
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

    def __init__(self, *styles: int, fmt: str = "{}") -> None:
        self._format = fmt
        self._list: list[int] = sorted(styles)
        self._style: tuple[str, str] = '\x1b[' + ';'.join(str(s) for s in self._list) + 'm', '\x1b[0m'
        self._codes: dict[str, int] = {Palette._get_type(code): code for code in self._list}

    @staticmethod
    def _get_type(code: int) -> str:
        prefix = (code - code%10) // 10
        typee = _names.get(prefix)
        if typee is None:
            raise InvalidCode(f"Invalid type with prefix '{prefix}'")
        return typee

    def print(self, text: str) -> None:
        print(self(text))

    def __call__(self, text: str) -> str:
        return self._format.format(text).join(self._style)

    def __ixor__(self, other: int) -> Self:
        # NOTE may be bugged, no _codes redefined
        if other in self._list:
            self._list.remove(other)
        else:
            self._list.append(other)
        self._style = '\x1b[' + ';'.join(str(s) for s in self._list) + 'm', '\x1b[0m'
        return self

    def __iadd__(self, other: int) -> Self:
        _new = {Palette._get_type(other): other}
        self._codes.update(_new)
        self._list = list(self._codes.values())
        self._style = '\x1b[' + ';'.join(str(s) for s in self._list) + 'm', '\x1b[0m'
        return self

    def __add__(self, other: int) -> Palette:
        _new = {Palette._get_type(other): other}
        _copy = self._codes.copy()
        _copy.update(_new)
        _list = _copy.values()
        return self.__class__(*_list)

    def __or__(self, other: Palette) -> Palette:
        _new = {Palette._get_type(code): code for code in other._list}
        _copy = self._codes.copy()
        _copy.update(_new)
        _list = _copy.values()
        return self.__class__(*_list)

    def __len__(self) -> int:
        return len(self._list)

class Color:
    black = Palette(FORE.BLACK)
    red = Palette(FORE.RED)
    green = Palette(FORE.GREEN)
    yellow = Palette(FORE.YELLOW)
    blue = Palette(FORE.BLUE)
    magenta = Palette(FORE.MAGENTA)
    cyan = Palette(FORE.CYAN)
    white = Palette(FORE.WHITE)

    lightblack = Palette(FORE.LIGHT.BLACK)
    lightred = Palette(FORE.LIGHT.RED)
    lightgreen = Palette(FORE.LIGHT.GREEN)
    lightyellow = Palette(FORE.LIGHT.YELLOW)
    lightblue = Palette(FORE.LIGHT.BLUE)
    lightmagenta = Palette(FORE.LIGHT.MAGENTA)
    lightcyan = Palette(FORE.LIGHT.CYAN)
    lightwhite = Palette(FORE.LIGHT.WHITE)
