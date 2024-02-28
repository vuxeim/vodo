from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stages import Stage
    from typing import Callable

from keyboard import key
from util import ASSERT

class Handler:

    def __init__(self, stage: Stage):
        self.stage = stage
        self.functions = _Functions(stage)
        self._reactions = dict()

        self._register(key.Q, self.functions.quit)
        self._register(key.J, self.functions.move_down)
        self._register(key.K, self.functions.move_up)
        self._register(key.D, self.functions.delete)
        self._register(key.TAB, self.functions.switch_tab)
        self._register(key.SPACE, self.functions.quick_toggle)
        self._register(key.SHIFT_J, self.functions.rotate, kpass=True)
        self._register(key.SHIFT_K, self.functions.rotate, kpass=True)
        self._register(key.DOWN, self.functions.move_down)
        self._register(key.UP, self.functions.move_up)
        self._register(key.SHIFT_DOWN, self.functions.rotate, kpass=True)
        self._register(key.SHIFT_UP, self.functions.rotate, kpass=True)
        self._register(key.ENTER, self.functions.toggle, kpass=True)
        self._register(key.E, self.functions.input, kpass=True)
        self._register(key.N, self.functions.input, kpass=True)

    def _register(self, key: str, fun: Callable, kpass: bool = False, once=True) -> None:
        """
        Register callback to a key.
        kpass - pass pressed key as an argument
        once - prevent event from propagating further
        """
        self._reactions.update({key: (lambda: fun(key) if kpass else fun(), once)})

    def react(self) -> None:
        for assigned_key, (fun, once) in self._reactions.items():
            if self.stage.kb.is_pressed(assigned_key, once=once):
                fun()

class _Functions:

    def __init__(self, stage: Stage):
        self.stage = stage

    def move_down(self):
        index = self.stage.list.index+1
        size = self.stage.list.items.last_index
        self.stage.list.index = min(index, size)

    def move_up(self):
        index = self.stage.list.index-1
        self.stage.list.index = max(0, index)

    def rotate(self, pressed_key: str):
        direction = {key.SHIFT_K: 'up',
                     key.SHIFT_UP: 'up',
                     key.SHIFT_J: 'down',
                     key.SHIFT_DOWN: 'down'}.get(pressed_key)
        ASSERT(direction is not None, "Unsupported key", pressed_key)
        self.stage.list.rot(direction)

    def toggle(self, pressed_key: str):
        value = {key.D: True, key.U: False}.get(pressed_key)
        self.stage.list.toggle(value=value)

    def quick_toggle(self) -> None:
        self.stage.list.toggle()
        self.move_down()

    def quit(self) -> None:
        self.stage.app.switch_stage("mainmenu")

    def delete(self) -> None:
        self.stage.list.delete()

    def input(self, pressed_key: str):
        self.stage.editor.activate(clear=True)
        if pressed_key == key.E:
            self.stage.editor.load(self.stage.list.current().text)
        elif pressed_key == key.N:
            self.stage.list.new()

    def switch_tab(self) -> None:
        self.stage.app.switch_stage("passmgr")

