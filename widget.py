from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screen import Screen

import colorman as cm
from vector import Vec2

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

class Text:

    def __init__(self, text: str):
        self.text = text
        self.color = cm.Palette(cm.FORE.MAGENTA)
        self.pos: Vec2 = Vec2.new()
        self.counter = 0
        self.blink = True
        self.blink_speed = 1

    def toggle_color(self) -> None:
        self.color ^= cm.STYLE.BOLD

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.text))

