# https://stackoverflow.com/questions/35772001/how-to-handle-a-signal-sigint-on-a-windows-os-machine
from __future__ import annotations
from time import sleep, perf_counter
from os import get_terminal_size

import colorman as cm
from colorman import Color
from keyboard import Keyboard
from screen import Screen
from vector import Vec2
from util import fprint

class App:

    def __init__(self) -> None:
        self.kb: Keyboard = Keyboard()
        self.screen: Screen = Screen(lambda: Vec2(*get_terminal_size()))

        self._running: bool = True
        self._TPS: float = 1/30
        self.dt: float = 0.0
        self._prev_time: float = perf_counter()
        self._now: float = 0.0

    def request_quit(self) -> None:
        self._running = False

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
        pass

    def _render(self) -> None:
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

