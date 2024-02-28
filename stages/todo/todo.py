from stages.stage import Stage
from .list import TList
from vector import Vec2
from colorman import Color
from keyboard import key
from widget import Button
from .handler import Handler
from .ui import Layout


class TodoStage(Stage):

    FILE_NAME = "tasks"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.list: TList = TList(self.editor)
        self.layout = Layout()
        self.handler = Handler(self)
        self.buttons: list[Button] = self.layout.get_buttons()
        self.list.load(self.FILE_NAME)

    def render(self) -> None:
        self.layout.render(self.app.screen)
        self.list.render(self.app.screen)

    def process(self) -> None:
        self.layout.process()
        self.list.process(self.screen.size)

        # Remove current entry if the entry is empty
        if not self.editor.is_active():
            if self.list.size.y > 0:
                if self.list.items[self.list.index].text == '':
                    self.list.delete()

        # Update editor position and cursor position
        self.editor.pos = self.list.pos+Vec2(0, self.list.index)
        self.editor.process()

        # Animate button press
        for btn in self.buttons:
            btn.counter += self.app._TPS + self.app.dt
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

        self.handler.react()

    def exit(self) -> None:
        self.list.save()

