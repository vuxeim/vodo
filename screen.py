import re
from typing import Callable


from vector import Vec2
from util import pprint


class Screen:

    PATTERN = re.compile('\x1b.*?m')

    def __init__(self, get_size_fun: Callable) -> None:
        self._get_size_fun: Callable = get_size_fun
        self.size: Vec2 = self._get_size_fun()
        self._buf: Buffer = Buffer(self.size)
    
    def clear(self) -> None:
        self._buf.clear()
    
    def write(self, pos: Vec2, content: str) -> None:
        text = Screen.PATTERN.sub('', content)
        code = Screen.PATTERN.findall(content)
        self._buf.write(pos, text)
        if code:
            self._buf.color(pos, code.pop(0), len(text))
    
    def update(self) -> None:
        new_size = self._get_size_fun()
        if new_size != self._buf._size:
            self._resize(new_size)
            self.size = new_size
    
    def _resize(self, new_size: Vec2) -> None:
        self._buf.resize_by(new_size - self._buf._size)
    
    def flush(self) -> None:
        self._buf.print_to_stdout()
    

class Buffer:

    def __init__(self, size: Vec2) -> None:
        self._size = size
        self._lines: list[_BufLine] = [_BufLine(size.x) for _ in range(size.y)]

    def color(self, pos: Vec2, code: str, size: int) -> None:
        self._lines[pos.y].color(code, pos.x, size)

    def write(self, pos: Vec2, text: str) -> None:
        """ Write given text to buffer at certain position """
        self._lines[pos.y][pos.x] = text
    
    def print_to_stdout(self) -> None:
        for num, line in enumerate(self._lines, start=1):
            pprint(0, num, line.compile())
    
    def resize_by(self, diff: Vec2) -> None:
        
        if diff.x != 0:
            for line in self._lines:
                line.resize_by(diff.x)

        if diff.y > 0:
            self._lines.extend([_BufLine(self._size.x+diff.x) for _ in range(diff.y)])

        elif diff.y < 0:
            self._lines = self._lines[:diff.y]
        
        self._size += diff
    
    def clear(self) -> None:
        for line in self._lines:
            line.clear()


class _BufLine:

    def __init__(self, length: int) -> None:
        self._len = length
        self._data: str = ' '*self._len
        self._colors: dict[int, code] = {}
        self._resets: dict[int, bool] = {}
    
    def __setitem__(self, index: int, value: str):
        self._data = self._data[:index] + value + self._data[index+len(value):]

    def color(self, code: str, offset: int, size: int) -> None:
        self._colors[offset] = code
        self._resets[offset+size-1] = True

    def compile(self) -> str:
        return ''.join(self._colors.get(idx, '') + char + '\x1b[0m'*self._resets.get(idx, False) for idx, char in enumerate(self._data))
    
    def resize_by(self, diff: int) -> None:

        if diff == 0:
            return

        if diff > 0:
            self._data = self._data + ' '*diff
        
        elif diff < 0:
            self._data = self._data[:diff]
        
        self._len += diff

    def clear(self) -> None:
        self._data = ' '*self._len
        self._colors.clear()
        self._resets.clear()
