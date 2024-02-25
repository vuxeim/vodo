from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screen import Screen
    from keyboard import Keyboard
from keyboard import key
from vector import Vec2
import colorman as cm
from util import ASSERT, fprint

class Editor:

    def __init__(self, keyboard: Keyboard):
        self.kb: Keyboard = keyboard
        self.color = cm.Color.lightwhite
        self.pos: Vec2 = Vec2.new()
        self.content: list[str] = []
        self.index: int = self.last_index
        self._active: bool = False

    @property
    def last_index(self) -> int:
        return len(self.content)

    @property
    def text(self):
        return "".join(self.content)

    def handle(self, char: str) -> None:
        if char == key.DELETE:
            if self.index < self.last_index:
                self.content.pop(self.index)
        elif char == key.BACKSPACE:
            if self.index > 0:
                self.content.pop(self.index-1)
                self.index -= 1
        elif char == key.LEFT:
            self.index = max(0, self.index-1)
        elif char == key.RIGHT:
            self.index = min(self.last_index, self.index+1)
        elif char.isprintable():
            self.content.insert(self.index, char)
            self.index += 1

    def load(self, text: str) -> None:
        self.content = [*text]
        self.index = self.last_index

    def is_active(self) -> bool:
        return self._active

    def activate(self, clear: bool = False) -> None:
        if clear:
            self.content = []
            self.index = self.last_index
        ASSERT(not self._active, "Activating already active editor")
        self._active = not self._active
        self.kb.start_capture()
        fprint(cm.CURSOR.SHOW)

    def deactivate(self) -> None:
        ASSERT(self._active, __file__+" Deactivating already inactive editor")
        self._active = not self._active
        self.kb.stop_capture()
        fprint(cm.CURSOR.HIDE)

    def render(self, screen: Screen) -> None:
        """ Renders only if it's active """
        if not self.is_active():
            return
        screen.write(self.pos, self.color(self.text))

