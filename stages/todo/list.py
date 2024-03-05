from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screen import Screen
    from editor import Editor
import colorman as cm
from vector import Vec2
from widgets import Box
from util import ASSERT

class _Entry:

    fmt = '[{}] {}'
    marks = {False: '_', True: '\u2713'}

    def __init__(self, content: str, done: bool):
        self.text: str = content.strip()
        self.done: bool = done

    @property
    def length(self) -> int:
        return len(self.compose())

    def set(self, value: bool) -> None:
        self.done = value

    def toggle(self) -> None:
        self.done = not self.done

    def compose(self) -> str:
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
        ASSERT(off is not None, "Unsupported direction", direction)
        tempid = (index+off)%self.size
        temp = self[tempid]
        self[tempid] = self[index]
        self[index] = temp

class TList:

    NORMAL = cm.Palette(cm.FORE.LIGHT.YELLOW)
    ACTIVE = NORMAL + cm.STYLE.REVERSE
    DONE = cm.Palette(cm.FORE.GREEN)

    def __init__(self, editor: Editor) -> None:
        self.editor = editor
        self.file: str = ""
        self.items: _List[_Entry] = _List()
        self.prev_index: int = 0
        self.index: int = 0
        self.counter = 0
        self.pos: Vec2 = Vec2.new()
        self.size: Vec2 = Vec2.new()
        self.box: Box = Box()

    def process(self, screen_size: Vec2) -> None:
        # Center the todo list
        if len(self.items) > 0:
            length = max(entry.length for entry in self.items)
            if self.editor.is_active():
                length = max(self.editor.index, length)
            self.size = Vec2(length, len(self.items))
        else:
            self.size = Vec2(0, 0)
        self.pos = screen_size/2 - self.size/2

        # Update the todo list border
        padding = Vec2(1, 0)
        size_offset = padding + Vec2(2, 2)
        self.box.size = self.size + size_offset + padding
        self.box.pos = self.pos - Vec2(1, 1) - padding

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
        self.box.render(screen)
        for idx, item in enumerate(self.items):
            if self.editor.is_active() and idx == self.index:
                continue
            screen.write(self.pos+Vec2(0, idx), self._get_color(item, idx)(item.compose()))

    def save(self) -> None:
        with open(self.file, 'wt', encoding='utf8') as f:
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
        ASSERT(drc in (_List.DOWN, _List.UP), "Direction must be UP or DOWN", drc)
        off = {_List.DOWN: 1, _List.UP: -1}.get(drc)
        new_index = (self.index+off)%self.size.y

        if self.index == self.items.last_index and new_index == 0:
            self.items.shift('down')
        elif self.index == 0 and new_index == self.items.last_index:
            self.items.shift('up')
        else:
            self.items.swap(self.index, drc)

        self.index = new_index

