from __future__ import annotations
from typing import TYPE_CHECKING, Callable

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

    def update_position(self, screen_size: Vec2) -> None:
        if self.position == "center,center":
            self.pos = screen_size//2 - Vec2(len(self)//2, 0)
        elif self.position == "bottom,left":
            self.pos = Vec2(0, screen_size.y-1)
        elif self.position == "bottom,right":
            self.pos = Vec2(screen_size.x-len(self), screen_size.y-1)
        else:
            self.pos = Vec2.new()

class Clock(PositionedText):

    def __init__(self, position: str, get_time_func: Callable) -> None:
        super().__init__(text="", position=position)
        self.offset = Vec2.new()
        self.get_time_func = get_time_func

    def update(self) -> None:
        now = self.get_time_func()
        self.text = ":".join(map(lambda i: str(i).zfill(2), (now.tm_hour, now.tm_min, now.tm_sec)))

    def update_position(self, screen_size: Vec2) -> None:
        super().update_position(screen_size)
        self.pos += self.offset

class Box:

    class F:
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
        # TODO make it more readable
        screen.write(self.pos, self.color(self.F.tl+(self.F.hor*(self.size.x-2))+self.F.tr))
        for i in range(1, self.size.y-1):
            screen.write(self.pos+Vec2(0, i), self.color(self.F.ver))
            screen.write(self.pos+Vec2(self.size.x-1, i), self.color(self.F.ver))
        screen.write(self.pos+Vec2(0, self.size.y-1),
                     self.color(self.F.bl+(self.F.hor*(self.size.x-2))+self.F.br))

