#https://stackoverflow.com/questions/35772001/how-to-handle-a-signal-sigint-on-a-windows-os-machine
from __future__ import annotations
from time import sleep, perf_counter_ns

import colorman as cm
from colorman import Color
from keyboard import Keyboard, key
from screen import Screen
from list import TList
from widget import Button, Text
import util

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
    
    def toggle(self, pressed_key: str):
        value = {key.D: True, key.U: False}.get(pressed_key)
        self.app.list.toggle(value=value)

    def quick_toggle(self):
        self.app.list.toggle()
        self.move_down()

class App:

    TARGET_TPS: int = 20

    def __init__(self) -> None:
        self.kb = Keyboard()
        self.screen = Screen()
        self.list: TList = TList((0, 6))
        self.text = Text('TODO', (0, 4))
        self.fun = Fun(self)
        self.buttons = (
                Button(key.N, '(n) New', (0, 0)),
                Button(key.D, '(d) Done', (9, 0)),
                Button(key.U, '(u) Undone', (19, 0)),
                Button(key.SPACE, '(space) Toggle', (31, 0)),
                Button(key.E, '(e) Edit', (47, 0)),
                Button(key.O, '(o) Load', (57, 0)),
                Button(key.Q, '(q) Quit', (67, 0)),
                Button(key.ESC, '(esc) Quit', (77, 0)),

                Button(key.K, '(k) Up', (0, 1)),
                Button(key.J, '(j) Down', (8, 1)),
                Button(key.SHIFT_K, '(K) Move Up', (24, 1)),
                Button(key.SHIFT_J, '(J) Move Down', (43, 1)),

                Button(key.UP, '(↑) Up', (0, 2)),
                Button(key.DOWN, '(↓) Down', (8, 2)),
                Button(key.SHIFT_UP, '(shift ↑) Move Up', (18, 2)),
                Button(key.SHIFT_DOWN, '(shift ↓) Move Down', (37, 2)),
                )
        self.running = True
        self.tps: int = int(1/self.TARGET_TPS*1e9)
        self.delta: int = 0
        self.prev_time: int = perf_counter_ns()

    def load(self, file: str) -> None:
        self.list.load(file)

    def run(self) -> None:
        print(cm.BUFFER.ALT, end='')
        print(cm.CURSOR.HIDE, end='')
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

        if self.kb.is_pressed(key.Q):
            self.running = False
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
        if self.kb.is_pressed(key.U, once=False):
            self.fun.toggle(key.U)
        if self.kb.is_pressed(key.D, once=False):
            self.fun.toggle(key.D)

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

        self.kb.clear()

    def render(self) -> None:
        for btn in self.buttons:
            btn.render(self.screen)
        self.list.render(self.screen)
        self.text.render(self.screen)
        self.screen.update()
        self.screen.flush()

    def exit(self, e: BaseException | None = None) -> None:
        print(cm.BUFFER.NORMAL, end='')
        print(cm.CURSOR.SHOW, end='')
        if isinstance(e, KeyboardInterrupt):
            print(Color.lightgreen('^C ... Work saved'))
            return
        print(Color.lightgreen('Work saved'))

def main():
    app = App()
    app.load('tasks')
    app.run()

if __name__ == "__main__":
    main()

