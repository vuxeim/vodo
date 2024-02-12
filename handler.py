from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import App

from keyboard import key
import colorman as cm
from util import fprint

class Handler:

    def __init__(self, app: App):
        self.app = app
        self.functions = _Functions(app)
        self._reactions = dict()

        self._register(key.Q, self.functions.quit)
        self._register(key.J, self.functions.move_down)
        self._register(key.K, self.functions.move_up)
        self._register(key.SPACE, self.functions.quick_toggle)
        self._register(key.SHIFT_J, self.functions.rotate, kpass=True)
        self._register(key.SHIFT_K, self.functions.rotate, kpass=True)
        self._register(key.DOWN, self.functions.move_down)
        self._register(key.UP, self.functions.move_up)
        self._register(key.SHIFT_DOWN, self.functions.rotate, kpass=True)
        self._register(key.SHIFT_UP, self.functions.rotate, kpass=True)
        self._register(key.ENTER, self.functions.toggle)
        self._register(key.E, self.functions.input)

    def _register(self, key: Key, fun: Callable, kpass: bool = False, once=True) -> None:
        """
        Register callback to a key.
        kpass - pass pressed key as an argument
        once - prevent event from propagating further
        """
        self._reactions.update({key: (lambda: fun(key) if kpass else fun(), once)})

    def react(self) -> None:
        for key, (fun, once) in self._reactions.items():
            if self.app.kb.is_pressed(key, once=once):
                fun()

class _Functions:

    def __init__(self, app: App):
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
        self.app.editor.clear()
        fprint(cm.CURSOR.SHOW)

    def normal(self):
        self.app.kb.normal_mode()
        fprint(cm.CURSOR.HIDE)

