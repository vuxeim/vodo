#https://stackoverflow.com/questions/35772001/how-to-handle-a-signal-sigint-on-a-windows-os-machine
from __future__ import annotations
from time import sleep, perf_counter_ns

import colorman as cm
from colorman import Color
from keyboard import Keyboard, key
from screen import Screen
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

        self.text.text = sorted(self.list.done)
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

class Button:

    def __init__(self, key: str, name: str, pos: tuple[int, int]) -> None:
        self.key = key
        self.name = name
        self.color = Color.lightwhite
        self.pos = pos
        self.counter = 0

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.name))

class Text:

    def __init__(self, text: str, pos: tuple[int, int]) -> None:
        self.text = text
        self.color = cm.Palette(cm.FORE.MAGENTA)
        self.pos = pos
        self.counter = 0
        self.blink = False
        self.blink_speed = 1

    def toggle_color(self) -> None:
        self.color ^= cm.STYLE.BOLD

    def render(self, screen: Screen) -> None:
        screen.write(self.pos, self.color(self.text))

class TList:

    ACTIVE = cm.Palette(cm.FORE.BLACK, cm.BACK.WHITE)
    DONE = cm.Palette(cm.FORE.GREEN)
    NORMAL = cm.Palette(cm.FORE.YELLOW)

    def __init__(self, pos: tuple[int, int]) -> None:
        self.items: list[str] = []
        self.index: int = 0
        self.pos: tuple[int, int] = pos
        self.size: int = 0
        self.done: set[int] = set()

    def load(self, file: str) -> None:
        with open(file, encoding='utf8') as f:
            self.items = [line.strip() for line in f.readlines() if line.strip()]
        self.size = len(self.items)

    def render(self, screen: Screen) -> None:
        x,y = self.pos
        for idx, item in enumerate(self.items):
            text = '[{}] {}'.format('x' if idx in self.done else ' ', item)
            screen.write((x, y), self._get_color(idx)(text))
            y += 1

    def _get_color(self, index: int):
        if index == self.index:
            if index in self.done:
                return TList.DONE | TList.ACTIVE
            return TList.ACTIVE
        if index in self.done:
            return TList.DONE
        return TList.NORMAL

    def toggle(self, value: bool | None = None) -> None:
        if value is not None:
            if value:
                self.done.add(self.index)
            else:
                self.done.discard(self.index)
            return

        if self.index in self.done:
            self.done.remove(self.index)
            return
        self.done.add(self.index)

    def rotold(self, drc: str) -> None:
        off = {'down': 1, 'up': -1}.get(drc, 0)
        nid = self.index+off
        if nid < 0 or nid > self.size-1:
            return

        if nid in self.done and self.index not in self.done:
            self.done.remove(nid)
            self.done.add(self.index)
        elif nid not in self.done and self.index in self.done:
            self.done.remove(self.index)
            self.done.add(nid)

        neigh = self.items[nid]
        self.items[nid] = self.items[self.index]
        self.items[self.index] = neigh
        self.index += off

    def rot(self, drc: str) -> None:
        off = {'down': 1, 'up': -1}.get(drc, 0)
        nid = (self.index+off)%self.size

        # if nid in self.done and self.index not in self.done:
        #     self.done.remove(nid)
        #     self.done.add(self.index)
        # elif nid not in self.done and self.index in self.done:
        #     self.done.remove(self.index)
        #     self.done.add(nid)
        if self.index-nid == self.size-1:
            self.items.insert(0, self.items.pop())
            self.done = {x+1 if x not in (self.size-1,) else x for x in self.done}
        elif self.index-nid == -(self.size-1):
            self.items.append(self.items.pop(0))
            self.done = {x-1 if x not in (0,) else x for x in self.done}
        else:
            neigh = self.items[nid]
            self.items[nid] = self.items[self.index]
            self.items[self.index] = neigh

        self.index = (self.index+off)%self.size


def main():
    app = App()
    try:
        app.load('/vodo/tasks')
    except FileNotFoundError:
        app.load('tasks')
    app.run()

if __name__ == "__main__":
    main()

