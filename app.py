#https://stackoverflow.com/questions/35772001/how-to-handle-a-signal-sigint-on-a-windows-os-machine
from __future__ import annotations
from time import sleep, perf_counter_ns

import colorman as cm
from colorman import Color
from keyboard import Keyboard, key
from screen import Screen
from fun import Fun
from ui import Layout
from list import TList
from widget import Button, Text, Box
from vector import Vec2
import util


class App:

    TARGET_TPS: int = 20

    def __init__(self) -> None:
        self.kb = Keyboard()
        self.screen = Screen()
        self.fun = Fun(self)
        self.layout = Layout(self.screen.size)
        self.list: TList = TList(Vec2(2, 6))
        self.text = Text('TODO')
        self.text.pos = Vec2(0, self.screen.size.y-1)
        self.buttons: list[Button] = self.layout.get_buttons()
        self.running = True
        self.tps: int = int(1/self.TARGET_TPS*1e9)
        self.delta: int = 0
        self.prev_time: int = perf_counter_ns()

    def load(self, file: str) -> None:
        self.list.load(file)

    def run(self) -> None:
        util.fprint(cm.BUFFER.ALT)
        util.fprint(cm.CURSOR.HIDE)
        try:
            while self.running:
                self.screen.clear()

                wait = max(0, self.tps - self.delta)
                sleep(wait/1e9)
                self.now = perf_counter_ns()
                self.delta = self.now - self.prev_time - wait
                self.prev_time = self.now

                self.process()
                self.render()
        except KeyboardInterrupt as e:
            self.exit(e)
        else:
            self.exit()

    def process(self) -> None:

        self.layout.calculate()
        self.text.pos = Vec2(0, self.screen.size.y-1)

        if self.kb.is_pressed(key.Q):
            self.fun.quit()
        if self.kb.is_pressed(key.J, once=False):
            self.fun.move_down()
        if self.kb.is_pressed(key.K, once=False):
            self.fun.move_up()
        if self.kb.is_pressed(key.SPACE, once=False):
            self.fun.quick_toggle()
        if self.kb.is_pressed(key.SHIFT_J, once=False):
            self.fun.rotate(key.SHIFT_J)
        if self.kb.is_pressed(key.SHIFT_K, once=False):
            self.fun.rotate(key.SHIFT_K)
        if self.kb.is_pressed(key.DOWN, once=False):
            self.fun.move_down()
        if self.kb.is_pressed(key.UP, once=False):
            self.fun.move_up()
        if self.kb.is_pressed(key.SHIFT_DOWN, once=False):
            self.fun.rotate(key.SHIFT_DOWN)
        if self.kb.is_pressed(key.SHIFT_UP, once=False):
            self.fun.rotate(key.SHIFT_UP)
        if self.kb.is_pressed(key.ENTER, once=False):
            self.fun.toggle()

        for btn in self.buttons:
            btn.counter += self.tps+self.delta
            if self.kb.is_pressed(btn.key):
                btn.counter = 0
                btn.color = Color.green
            if btn.counter > 0.2 * 1e9:
                btn.counter = 0
                btn.color = Color.lightwhite

        self.text.counter += self.tps+self.delta
        if self.text.blink:
            if self.text.counter > self.text.blink_speed * 1e9:
                self.text.counter = 0
                self.text.toggle_color()

        # self.kb.clear()

    def render(self) -> None:
        self.layout.render(self.screen)
        self.list.render(self.screen)
        self.text.render(self.screen)
        self.screen.update()
        self.screen.flush()

    def request_quit(self) -> None:
        self.running = False

    def exit(self, e: KeyboardInterrupt | None = None) -> None:
        util.fprint(cm.BUFFER.NORMAL)
        util.fprint(cm.CURSOR.SHOW)
        if isinstance(e, KeyboardInterrupt):
            print(Color.lightgreen('^C ... Work saved'))
            return
        print(Color.lightgreen('Work saved'))

