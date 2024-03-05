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
        self.color = cm.Color.lightblack
        self.pos: Vec2 = Vec2.new()
        self.counter: float = 0.0
        self.blink_time: float = 0.26

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.text))


