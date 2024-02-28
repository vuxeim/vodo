# https://stackoverflow.com/questions/35772001/how-to-handle-a-signal-sigint-on-a-windows-os-machine
from __future__ import annotations
from time import sleep, perf_counter
from os import get_terminal_size

import colorman as cm
from colorman import Color
from keyboard import Keyboard
from screen import Screen
from editor import Editor
from vector import Vec2
from util import fprint, ASSERT

from stages import Stage
from stages import MainMenu
from stages import TodoStage
from stages import PasswordManager
from stages import TankeStelle

class App:

    def __init__(self) -> None:
        self.kb: Keyboard = Keyboard()
        self.screen: Screen = Screen(lambda: Vec2(*get_terminal_size()))
        self.editor: Editor = Editor(self.kb)
        self._running: bool = True
        self._TPS: float = 1/30
        self.dt: float = 0.0
        self._prev_time: float = perf_counter()
        self._now: float = 0.0

        class _stages:
            mainmenu = MainMenu(self)
            todo = TodoStage(self)
            passmgr = PasswordManager(self)
            tanke = TankeStelle(self)

        self._stages = _stages
        self._stage: Stage = self._stages.mainmenu

    def request_quit(self) -> None:
        self._stage.exit()
        self._running = False

    def switch_stage(self, new_stage: str) -> None:
        stage = {"mainmenu": self._stages.mainmenu,
                 "todo": self._stages.todo,
                 "passmgr": self._stages.passmgr,
                 "tanke": self._stages.tanke}.get(new_stage)
        self._stage.exit()
        ASSERT(isinstance(stage, Stage), f"Unknown stage name '{new_stage}'")
        self._stage = stage
        self._stage.process()

    def run(self) -> None:
        fprint(cm.BUFFER.ALT+cm.CURSOR.HIDE)
        try:
            while self._running:
                self.screen.clear()

                wait = max(0, self._TPS - self.dt)
                sleep(wait)
                self._now = perf_counter()
                self.dt = self._now - self._prev_time - wait
                self._prev_time = self._now

                self._process()
                self._render()
        except (KeyboardInterrupt, AssertionError) as e:
            self._exit(e)
        else:
            self._exit()

    def _process(self) -> None:
        self._stage.process()
        self.editor.process()

        # Consume all the other button press events
        if not self.editor.is_active():
            self.kb.clear()

    def _render(self) -> None:
        self._stage.render()
        self.editor.render(self.screen)
        self.screen.update()
        self.screen.flush()

    def _exit(self, e: BaseException | None = None) -> None:
        self.request_quit()
        fprint(cm.BUFFER.NORMAL+cm.CURSOR.SHOW)
        if isinstance(e, KeyboardInterrupt):
            print(Color.lightgreen('^C ... Work saved'))
        elif isinstance(e, AssertionError):
            print(e.args[0])
        else:
            print(Color.lightgreen('Work saved'))

