from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screen import Screen
from vector import Vec2
import colorman as cm

class Text:

    def __init__(self, text: str):
        self.text = text
        self.color = cm.Palette(cm.FORE.MAGENTA, cm.STYLE.BOLD)
        self.pos: Vec2 = Vec2.new()
        self.counter = 0
        self.blink_time = 0.5
        self.blink: bool = False

    def toggle(self) -> None:
        if self.blink:
            self.color ^= cm.STYLE.BOLD

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.text))

class PositionedText(Text):

    def __init__(self,
                 text: str,
                 position: str,
                 color: cm.Palette | None = None,
                 blink: bool = False,
                 *args, **kwargs) -> None:
        super().__init__(text, *args, **kwargs)
        self.position = position
        self.color = color or self.color
        self.blink = blink
        self.blink_time = 0.5

    def __len__(self) -> int:
        return len(self.text)

    def toggle(self):
        if self.blink:
            self.color ^= cm.STYLE.BOLD

    def process(self, screen_size: Vec2) -> None:
        if self.position == "center,center":
            self.pos = screen_size//2 - Vec2(len(self)//2, 0)
        elif self.position == "top,center":
            self.pos = Vec2(screen_size.x//2 - len(self)//2, 0)
        elif self.position == "bottom,left":
            self.pos = Vec2(0, screen_size.y-1)
        elif self.position == "bottom,right":
            self.pos = Vec2(screen_size.x-len(self), screen_size.y-1)
        else:
            self.pos = Vec2.new()


