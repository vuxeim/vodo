from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screen import Screen

import colorman as cm
from vector import Vec2
from keyboard import key

class Button:

    def __init__(self, key: str, text: str):
        self.key = key
        self.text = text
        self.color = cm.Color.lightwhite
        self.pos: Vec2 = Vec2.new()
        self.counter = 0

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.text))

class Box:
    
    def __init__(self, pos: Vec2, size: Vec2):
        self.pos = pos
        self.size = size

    def render(self, screen: Screen):
        screen.write(self.pos, '-'*self.size.x)
        for i in range(1, self.size.y):
            screen.write(self.pos+Vec2(0, i), '|')
            screen.write(self.pos+Vec2(self.size.x-1, i), '|')
        screen.write(self.pos+Vec2(0, self.size.y-1), '-'*self.size.x)

class Editor:

    def __init__(self, pos: Vec2 = Vec2.new()):
        self.color = cm.Palette(cm.FORE.CYAN)
        self.pos: Vec2 = pos
        self.content: list[str] = []
        self.index = self.last_index

    @property
    def last_index(self) -> int:
        return max(0, len(self.content)-1)

    @property
    def text(self):
        return "".join(self.content)

    def handle(self, char: Key) -> None:
        if char == key.BACKSPACE:
            if self.index > 0:
                self.content.pop(self.index-1)
                self.index -= 1
        elif char == key.DELETE:
            if self.index < self.last_index:
                self.content.pop(self.index)
        elif char == key.LEFT:
            self.index = max(0, self.index-1)
        elif char == key.RIGHT:
            self.index = min(self.last_index, self.index+1)
        elif char.isprintable():
            self.content.insert(self.index, char)
            self.index+=1

    def clear(self) -> None:
        self.content = []
        self.index = self.last_index

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.text))

