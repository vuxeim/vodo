#https://stackoverflow.com/questions/35772001/how-to-handle-a-signal-sigint-on-a-windows-os-machine
from __future__ import annotations
from time import sleep, perf_counter_ns

import colorman as cm
from colorman import Color
from keyboard import Keyboard, key
from screen import Screen
from handler import Handler
from ui import Layout
from list import TList
from widget import Button, Editor, Box
from vector import Vec2
from util import fprint

class App:

    TARGET_TPS: int = 60

    def __init__(self) -> None:
        self.kb = Keyboard()
        self.screen = Screen()
        self.handler = Handler(self)
        self.layout = Layout(self.screen.size)
        self.list: TList = TList(Vec2(2, 6))
        self.editor = Editor()
        self.box = Box()
        self.buttons: list[Button] = self.layout.get_buttons()
        self.running = True
        self.tps: int = int(1/self.TARGET_TPS*1e9)
        self.dt: int = 0
        self.prev_time: int = perf_counter_ns()

    def load(self, file: str) -> None:
        self.list.load(file)

    def run(self) -> None:
        fprint(cm.BUFFER.ALT)
        fprint(cm.CURSOR.HIDE)
        try:
            while self.running:
                self.screen.clear()

                wait = max(0, self.tps - self.dt)
                sleep(wait/1e9)
                self.now = perf_counter_ns()
                self.dt = self.now - self.prev_time - wait
                self.prev_time = self.now

                self.process()
                self.render()
        except (KeyboardInterrupt, AssertionError) as e:
            self.exit(e)
        else:
            self.exit()

    def process(self) -> None:

        self.layout.calculate()
        self.list.calculate()

        self.editor.pos = self.list.pos+Vec2(4, self.list.index)
        pos = self.editor.pos+Vec2(self.editor.index+1, 1)
        fprint(cm.CURSOR(*pos.as_tuple()))

        self.list.pos = self.screen.size//2 - self.list.size//2

        self.box.pos = self.list.pos - Vec2(1, 1)
        self.box.size = self.list.size + Vec2(6, 2)

        # Animate button press
        for btn in self.buttons:
            btn.counter += self.tps+self.dt
            if not self.kb.capture:
                if self.kb.is_pressed(btn.key, once=False):
                    btn.counter = 0
                    btn.color = Color.green
            if btn.counter > 0.26 * 1e9:
                btn.counter = 0
                btn.color = Color.lightblack

        # Handle input mode
        if self.kb.capture:
            for char in self.kb.fetch():
                if char == key.ENTER:
                    self.handler.functions.normal()
                    self.list.editing = False
                    self.list.current().text = self.editor.text
                elif char == key.ESC:
                    self.handler.functions.normal()
                    self.list.editing = False
                else:
                    self.editor.handle(char)

        # Handle normal mode
        self.handler.react()

        # Consume all pressed button events
        for btn in self.buttons:
            _ = self.kb.is_pressed(btn.key)

    def render(self) -> None:
        self.layout.render(self.screen)
        self.list.render(self.screen)
        if self.kb.capture:
            self.editor.render(self.screen)
        self.box.render(self.screen)
        self.screen.update()
        self.screen.flush()

    def request_quit(self) -> None:
        self.running = False

    def exit(self, e: BaseException | None = None) -> None:
        fprint(cm.BUFFER.NORMAL)
        fprint(cm.CURSOR.SHOW)
        if isinstance(e, KeyboardInterrupt):
            print(Color.lightgreen('^C ... Work saved'))
            return
        if isinstance(e, AssertionError):
            print(Color.lightred(e))
            return
        print(Color.lightgreen('Work saved'))

