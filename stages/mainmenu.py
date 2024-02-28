from time import localtime

from stages.stage import Stage
from keyboard import key
from widget import PositionedText, Clock
from vector import Vec2
import colorman as cm

class MainMenu(Stage):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.texts = (PositionedText(text="Press ENTER to start...",
                                     blink=True,
                                     position="center,center",),
                      PositionedText(text="vuxeim",
                                     position="bottom,right",
                                     color=cm.Palette(cm.FORE.LIGHT.CYAN, cm.STYLE.BOLD),),
                      PositionedText(text="Press Q to exit...",
                                     position="bottom,left",
                                     color=cm.Palette(cm.FORE.RED, cm.STYLE.BOLD),),
                      )
        self.clock = Clock("center,center", localtime)
        self.clock.color = cm.Color.green
        self.clock.offset = Vec2(0, -2)

    def process(self) -> None:
        self.clock.update()
        self.clock.update_position(self.screen.size)
        for text in self.texts:
            text.update_position(self.screen.size)
            text.counter += self.app._TPS + self.app.dt
            if text.counter > text.blink_time:
                text.counter = 0
                text.toggle()
        if self.kb.is_pressed(key.ENTER):
            self.app.switch_stage("todo")
        if self.kb.is_pressed(key.Q):
            self.app.request_quit()

    def render(self) -> None:
        for text in self.texts:
            text.render(self.screen)
        self.clock.render(self.screen)

