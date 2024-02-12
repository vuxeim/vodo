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
        self.color = cm.Color.lightblack
        self.pos: Vec2 = Vec2.new()
        self.counter = 0

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.text))

class Box:
    
    class FRAME:
        tl = "┏"
        tr = "┓"
        bl = "┗"
        br = "┛"
        ver = "┃"
        hor = "━"

    def __init__(self, pos: Vec2 = Vec2.new(), size: Vec2 = Vec2.new()):
        self.pos = pos
        self.size = size
        self.color = cm.Color.lightblue

    def render(self, screen: Screen):
        screen.write(self.pos, self.color(self.FRAME.tl+(self.FRAME.hor*(self.size.x-2))+self.FRAME.tr))
        for i in range(1, self.size.y-1):
            screen.write(self.pos+Vec2(0, i), self.color(self.FRAME.ver))
            screen.write(self.pos+Vec2(self.size.x-1, i), self.color(self.FRAME.ver))
        screen.write(self.pos+Vec2(0, self.size.y-1), self.color(self.FRAME.bl+(self.FRAME.hor*(self.size.x-2))+self.FRAME.br))

class Editor:

    def __init__(self, pos: Vec2 = Vec2.new()):
        self.color = cm.Color.lightblack
        self.pos: Vec2 = pos
        self.content: list[str] = []
        self.index = self.last_index

    @property
    def last_index(self) -> int:
        return len(self.content)

    @property
    def text(self):
        return "".join(self.content)

    def handle(self, char: Key) -> None:
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
            self.index+=1

    def load(self, text: str) -> None:
        self.content = [*text]
        self.index = self.last_index

    def clear(self) -> None:
        self.content = []
        self.index = self.last_index

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.text))

