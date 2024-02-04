from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from screen import Screen

import colorman as cm

class Button:

    def __init__(self, key: str, name: str, pos: tuple[int, int]) -> None:
        self.key = key
        self.name = name
        self.color = cm.Color.lightwhite
        self.pos = pos
        self.counter = 0

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.name))

class Text:

    def __init__(self, text: str, pos: tuple[int, int]) -> None:
        self.text = text
        self.color = cm.Palette(cm.FORE.MAGENTA)
        self.pos = pos
        self.counter = 0
        self.blink = True
        self.blink_speed = 1

    def toggle_color(self) -> None:
        self.color ^= cm.STYLE.BOLD

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.text))

