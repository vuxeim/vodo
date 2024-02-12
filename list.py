from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screen import Screen
import colorman as cm
from vector import Vec2

class _Entry:
    
    fmt = '[{}] {}'
    marks = {False: ' ', True: 'x'}

    def __init__(self, content: str, done: bool):
        self.text: str = content.strip()
        self.done: bool = done

    def set(self, value: bool) -> None:
        self.done = value

    def toggle(self) -> None:
        self.done = not self.done

    def compose(self) -> None:
        return self.fmt.format(self.marks[self.done], self.text)

class _List(list):
    
    DOWN = 'down'
    UP = 'up'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def size(self):
        return len(self)

    @property
    def last_index(self):
        return self.size-1

    def shift(self, direction: str) -> None:
        """ Shift all elements in direction. Wrap around. """
        if direction == self.UP:
            self.append(self.pop(0))
        elif direction == self.DOWN:
            self.insert(0, self.pop())

    def swap(self, index: int, direction: str) -> None:
        """ Swap places element at index with the next element """
        off = {_List.DOWN: 1, _List.UP: -1}.get(direction)
        tempid = (index+off)%self.size
        temp = self[tempid]
        self[tempid] = self[index]
        self[index] = temp

class TList:

    ACTIVE = cm.Palette(cm.FORE.BLACK, cm.BACK.WHITE)
    DONE = cm.Palette(cm.FORE.GREEN)
    NORMAL = cm.Palette(cm.FORE.YELLOW)

    def __init__(self, pos: Vec2) -> None:
        self.file: str = ""
        self.editing = False
        self.items: _List[_Entry] = _List()
        self.prev_index: int = 0
        self.index: int = 0
        self.counter = 0
        self.pos: Vec2 = pos
        self.size: Vec2 = Vec2.new()
        self.done: set[int] = set()

    def calculate(self) -> None:
        self.size = Vec2(max((len(entry.text) for entry in self.items) or 1), len(self.items))

    def current(self) -> _Entry:
        return self.items[self.index]

    def load(self, file: str) -> None:
        self.file = file
        with open(file, encoding='utf8') as f:
            while line := f.readline():
                if not line:
                    continue
                done, text = line.split(';', maxsplit=1)
                self.items.append(_Entry(text, done=bool(done)))
        self.size.y = len(self.items)

    def new(self) -> None:
        self.prev_index = self.index
        self.items.append(_Entry('', done=False))
        self.index = self.items.last_index

    def delete(self) -> None:
        self.items.pop(self.index)
        self.index = max(0, self.index-1)

    def render(self, screen: Screen) -> None:
        x,y = self.pos.as_tuple()
        for idx, item in enumerate(self.items):
            if not self.editing or idx != self.index:
                screen.write(Vec2(x, y), self._get_color(item, idx)(item.compose()))
            y += 1

    def save(self) -> None:
        with open(self.file, 'wt') as f:
            f.write('\n'.join(('x'*entry.done)+';'+entry.text for entry in self.items))

    def _get_color(self, element: _Entry, index: int):
        if index == self.index:
            return TList.ACTIVE
        if element.done:
            return TList.DONE
        return TList.NORMAL

    def toggle(self, value: bool | None = None) -> None:
        self.items[self.index].toggle()
        if value is not None:
            self.items[self.index].set(value)

    def rot(self, drc: str) -> None:
        assert drc in (_List.DOWN, _List.UP)
        off = {_List.DOWN: 1, _List.UP: -1}.get(drc)
        new_index = (self.index+off)%self.size.y

        if self.index == self.items.last_index and new_index == 0:
            self.items.shift('down')
        elif self.index == 0 and new_index == self.items.last_index:
            self.items.shift('up')
        else:
            self.items.swap(self.index, drc)

        self.index = new_index

