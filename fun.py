from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import App

from keyboard import key
import colorman as cm
from util import fprint


class Fun:

    def __init__(self, app: App) -> None:
        self.app = app

    def move_down(self):
        index = self.app.list.index+1
        size = self.app.list.size-1
        self.app.list.index = min(index, size)

    def move_up(self):
        index = self.app.list.index-1
        self.app.list.index = max(0, index)

    def rotate(self, pressed_key: str):
        direction = {
                key.SHIFT_K: 'up',
                key.SHIFT_UP: 'up',
                key.SHIFT_J: 'down',
                key.SHIFT_DOWN: 'down'}.get(pressed_key)
        self.app.list.rot(direction)
    
    def toggle(self, pressed_key: str = ''):
        value = {key.D: True, key.U: False}.get(pressed_key)
        self.app.list.toggle(value=value)

    def quick_toggle(self):
        self.app.list.toggle()
        self.move_down()

    def quit(self):
        self.app.request_quit()

    def input(self):
        self.app.kb.input_mode()
        fprint(cm.CURSOR.SHOW)

    def normal(self):
        self.app.kb.normal_mode()
        self.app.buffer = ""
        fprint(cm.CURSOR.HIDE)

