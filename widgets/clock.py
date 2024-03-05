from __future__ import annotations
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from screen import Screen
from vector import Vec2
from .text import PositionedText

_b = r"""
 ,---.   ,--.  ,---. ,----.   ,---.,-----.  ,--. ,-----. ,---.  ,---.       \
/     \ /   | '.-.  \'.-.  | /    ||  .--' /  .' '--,  /|  o  ||  () \ .--. \
|  o  | `|  |  .-' .'  .' < /  '  |'--. `\|  .-.  .'  / .'   '.`._   | '--' \
\     /  |  | /   '-./'-'  |'--|  |.--'  /\   o |/   /  |  o  |  _> /  .--. \
 `---'   `--' '-----'`----'    `--'`----'  `---' `--'    `---'  `--'   '--' \
"""

_numbers = ["\n".join([l[7*x:7*x+7] for i, l in enumerate(_b.split("\n"))]) for x in range(10)]
_sep = "\n".join(l[70:76] for i, l in enumerate(_b.split("\n")))
_numbers.append(_sep)
_N = {}
for i in range(10):
    _N[str(i)] = _numbers[i]
_N[":"] = _numbers[10]

class Clock(PositionedText):

    NUMBERS = _N

    def __init__(self, position: str, get_time_func: Callable) -> None:
        super().__init__(text="", position=position)
        self.offset = Vec2.new()
        self.get_time_func = get_time_func
        self.style = "normal"
        self.buffer = _Buffer(Vec2(7*6+4*2, 5))

    @property
    def size(self) -> Vec2:
        return Vec2(self.buffer._size.x-4, 5)

    def process(self, screen_size: Vec2) -> None:
        t = self.get_time_func()
        self.text = ":".join(map(lambda i: str(i).zfill(2), (t.tm_hour, t.tm_min, t.tm_sec)))
        self.buffer.clear()
        x_pad = 0
        for i_x, char in enumerate(self.text):
            box = __class__.NUMBERS[char].strip('\n').split('\n')
            for i_y, line in enumerate(box):
                self.buffer.write(Vec2(x_pad, i_y), box[i_y])
            x_pad += len(box[0])

        super().process(screen_size)
        self.pos += self.offset

    def render(self, screen: Screen) -> None:
        if self.style == "normal":
            return super().render(screen)
        elif self.style == "big":
            for idx, line in enumerate(self.buffer.lines):
                screen.write(self.pos+Vec2(0, idx), self.color(line.data))

class _Buffer:

    def __init__(self, size: Vec2) -> None:
        self._size = size
        self.lines: list[_BufLine] = [_BufLine(size.x) for _ in range(size.y)]

    def write(self, pos: Vec2, text: str) -> None:
        """ Write given text to buffer at certain position """
        self.lines[pos.y][pos.x] = text

    def clear(self) -> None:
        for line in self.lines:
            line.clear()

class _BufLine:

    def __init__(self, length: int) -> None:
        self._len = length
        self.data: str = ' '*self._len

    def __setitem__(self, index: int, value: str):
        self.data = self.data[:index] + value + self.data[index+len(value):]

    def clear(self) -> None:
        self.data = ' '*self._len
