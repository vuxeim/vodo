from time import perf_counter, sleep, localtime
from os import get_terminal_size
from sys import argv

from keyboard import Keyboard, key
from screen import Screen
from vector import Vec2
from util import fprint
import colorman as cm
from widget import Clock

class App:

    def __init__(self) -> None:
        self.kb: Keyboard = Keyboard()
        self.screen: Screen = Screen(lambda: Vec2(*get_terminal_size()))

        # Timings
        self.dt: float = 0.0
        self._running: bool = True
        self._TPS: float = 1/30
        self._prev_time: float = perf_counter()
        self._now: float = 0.0

        # Widgets
        self.clock = Clock("center,center", localtime)
        self.clock.color = cm.Palette(cm.STYLE.BOLD, cm.FORE.LIGHT.MAGENTA)
        if len(argv) > 1:
            if argv[1] == "big":
                self.clock.style = "big"

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
        self.clock.update()
        self.clock.update_position(self.screen.size)
        if self.kb.is_pressed(key.Q):
            self.request_quit()

    def _render(self) -> None:
        self.clock.render(self.screen)
        self.screen.update()
        self.screen.flush()

    def _exit(self, e: BaseException | None = None) -> None:
        self.request_quit()
        fprint(cm.BUFFER.NORMAL+cm.CURSOR.SHOW)
        if isinstance(e, AssertionError):
            print(e.args[0])

def main() -> None:
    app = App()
    app.run()

if __name__ == "__main__":
    main()

