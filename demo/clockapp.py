from time import localtime
from sys import argv

from app import App as _App
from keyboard import key
from vector import Vec2
import colorman as cm
from widgets import Clock

class MyApp(_App):

    def __init__(self) -> None:
        super().__init__()

        self.clock = Clock("center,center", localtime)
        self.clock.color = cm.Palette(cm.STYLE.BOLD, cm.FORE.LIGHT.MAGENTA)
        self.clock.offset = Vec2(-self.clock.size.x//2, 0)
        if len(argv) > 1:
            if argv[1] == "big":
                self.clock.style = "big"

    def _process(self) -> None:
        self.clock.process(self.screen.size)
        if self.kb.is_pressed(key.Q):
            self.request_quit()

    def _render(self) -> None:
        self.clock.render(self.screen)
        super()._render()

def main() -> None:
    app = MyApp()
    app.run()

if __name__ == "__main__":
    main()

