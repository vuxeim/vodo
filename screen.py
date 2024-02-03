from os import get_terminal_size
import re


from vector import Vec2
import util


class Screen:

    PATTERN = re.compile('\x1b.*?m')

    def __init__(self) -> None:
        self.size = Vec2(*get_terminal_size())
        self._buf: Buffer = Buffer(self.size)
    
    def clear(self) -> None:
        self._buf.clear()
    
    def write(self, pos: Vec2, content: str) -> None:
        text = Screen.PATTERN.sub('', content)
        code = next(Screen.PATTERN.finditer(content)).group()
        self._buf.write(pos, text)
        self._buf.color(pos, code, len(text))
    
    def update(self) -> None:
        new_size = Vec2(*get_terminal_size())
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
        x, y = pos
        self._lines[y].color(code, x, size)

    def write(self, pos: Vec2, text: str) -> None:
        """ Write given text to buffer at certain position """
        x, y = pos
        self._lines[y][x] = text
    
    def print_to_stdout(self) -> None:
        for num, line in enumerate(self._lines, start=1):
            util.pprint(1, num, line.compile())
    
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
    
    def __setitem__(self, index: int, value: str):
        self._data = self._data[:index] + value + self._data[index+len(value):]

    def color(self, code: str, offset: int, size: int) -> None:
        self._colors[offset] = code
        self._colors[offset+size] = '\x1b[0m'

    def compile(self) -> str:
        return ''.join(self._colors.get(idx, '') + char for idx, char in enumerate(self._data))
    
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
