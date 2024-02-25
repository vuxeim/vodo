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
        self.blink_time = 0.26

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.text))

class Text:

    def __init__(self, text: str, pos: Vec2):
        self.text = text
        self.color = cm.Palette(cm.FORE.MAGENTA, cm.STYLE.BOLD)
        self.pos: Vec2 = pos
        self.counter = 0
        self.blink_time = 0.5

    def toggle(self) -> None:
        self.color ^= cm.STYLE.BOLD

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

