#https://stackoverflow.com/questions/35772001/how-to-handle-a-signal-sigint-on-a-windows-os-machine
from __future__ import annotations
from time import sleep, perf_counter

import colorman as cm
from colorman import Color
from keyboard import Keyboard, key
from screen import Screen
from handler import Handler
from ui import Layout
from list import TList
from widget import Button, Text
from editor import Editor
from vector import Vec2
from util import fprint

class App:

    TARGET_TPS: int = 30

    def __init__(self) -> None:
        self.kb: Keyboard = Keyboard()
        self.screen: Screen = Screen()
        self.handler: Handler = Handler(self)
        self.layout: Layout = Layout(self.screen.size)
        self.editor: Editor = Editor(self.kb)
        self.list: TList = TList(self.editor)
        self.buttons: list[Button] = self.layout.get_buttons()
        self.running: bool = True
        self.tps: float = 1/self.TARGET_TPS
        self.dt: float = 0.0
        self.prev_time: float = perf_counter()

    def load(self, file: str) -> None:
        self.list.load(file)

    def run(self) -> None:
        fprint(cm.BUFFER.ALT+cm.CURSOR.HIDE)
        try:
            while self.running:
                self.screen.clear()

                wait = max(0, self.tps - self.dt)
                sleep(wait)
                self.now = perf_counter()
                self.dt = self.now - self.prev_time - wait
                self.prev_time = self.now

                self.process()
                self.render()
        except (KeyboardInterrupt, AssertionError) as e:
            self.exit(e)
        else:
            self.exit()

    def process(self) -> None:
        # Recalculate sizes
        self.layout.calculate()
        self.list.calculate(self.screen.size)

        # Remove current entry if the entry is empty
        if not self.editor.is_active():
            if self.list.size.y > 0:
                if self.list.items[self.list.index].text == '':
                    self.list.delete()

        # Update editor position and cursor position
        self.editor.pos = self.list.pos+Vec2(0, self.list.index)
        pos = self.editor.pos+Vec2(self.editor.index+1, 1)
        fprint(cm.CURSOR(*pos.as_tuple()))

        # Animate button press
        for btn in self.buttons:
            btn.counter += self.tps+self.dt
            if not self.editor.is_active():
                if self.kb.is_pressed(btn.key, once=False):
                    btn.counter = 0
                    btn.color = Color.green
            if btn.counter > btn.blink_time:
                btn.counter = 0
                btn.color = Color.lightblack

        # Handle input mode
        if self.editor.is_active():
            for char in self.kb.fetch():
                if char == key.ENTER:
                    self.editor.deactivate()
                    self.list.current().text = self.editor.text
                elif char == key.ESC:
                    self.editor.deactivate()
                else:
                    self.editor.handle(char)

        # Handle normal mode
        self.handler.react()

        # Consume all the other button press events
        if not self.editor.is_active():
            self.kb.clear()

    def render(self) -> None:
        self.layout.render(self.screen)
        self.list.render(self.screen)
        self.editor.render(self.screen)
        self.screen.update()
        self.screen.flush()

    def request_quit(self) -> None:
        self.running = False

    def exit(self, e: BaseException | None = None) -> None:
        self.list.save()
        fprint(cm.BUFFER.NORMAL+cm.CURSOR.SHOW)
        if isinstance(e, KeyboardInterrupt):
            print(Color.lightgreen('^C ... Work saved'))
        elif isinstance(e, AssertionError):
            print(e.args[0])
        else:
            print(Color.lightgreen('Work saved'))

