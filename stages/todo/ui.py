from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screen import Screen

from keyboard import key
from widgets import Button
from vector import Vec2

class Layout:

    def __init__(self):
        self.buttons: tuple[tuple[Button, ...], ...] = ((
                    Button(key.TAB, '(tab) Switch tab'),
                ),
                (
                    Button(key.N, '(n) New'),
                    Button(key.E, '(e) Edit'),
                    Button(key.D, '(d) Delete'),
                    Button(key.O, '(o) Load'),
                    Button(key.Q, '(q) Quit'),
                ),
                (
                    Button(key.SPACE, '(space) Quict Toggle'),
                    Button(key.ENTER, '(enter) Toggle'),
                ),
                (
                    Button(key.K, '(k) Up'),
                    Button(key.J, '(j) Down'),
                    Button(key.SHIFT_K, '(K) Move Up'),
                    Button(key.SHIFT_J, '(J) Move Down'),
                ),
                (
                    Button(key.UP, '(↑) Up'),
                    Button(key.DOWN, '(↓) Down'),
                    Button(key.SHIFT_UP, '(shift ↑) Move Up'),
                    Button(key.SHIFT_DOWN, '(shift ↓) Move Down'),
                ))

    def process(self) -> None:
        occup = {i: 0 for i in range(len(self.buttons))}
        for ln, btns in enumerate(self.buttons):
            for btn in btns:
                occup[ln] += len(btn.text)

        for ln, btns in enumerate(self.buttons):
            off = 0
            for btn in btns:
                btn.pos = Vec2(off, ln)
                off += len(btn.text) + 3

    def render(self, screen: Screen):
        for btn in self.get_buttons():
            btn.render(screen)

    def get_buttons(self) -> list[Button]:
        return list(__class__.flatten(self.buttons))

    @staticmethod
    def flatten(data):
        if isinstance(data, tuple):
            for x in data:
                yield from __class__.flatten(x)
        else:
            yield data
