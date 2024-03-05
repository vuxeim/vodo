from app import App as _App
from keyboard import key
from editor import Editor
from widgets import Text
from vector import Vec2

class MyApp(_App):

    def __init__(self) -> None:
        super().__init__()

        self.text = Text("")
        self.text.pos = Vec2(10, 10)
        self.editor = Editor(self.kb)

    def _process(self) -> None:
        if self.kb.is_pressed(key.N):
            self.editor.activate(clear=True)
        if self.kb.is_pressed(key.R):
            self.editor.deactivate()
        if self.kb.is_pressed(key.Q):
            self.request_quit()

        if self.editor.is_active():
            for char in self.kb.fetch():
                if char == key.ENTER:
                    self.editor.deactivate()
                    self.text.text = self.editor.text
                elif char == key.ESC:
                    self.editor.deactivate()
                else:
                    self.editor.handle(char)

        self.editor.pos = self.text.pos
        self.editor.process()

    def _render(self):
        self.text.render(self.screen)
        self.editor.render(self.screen)
        super()._render()

def main() -> None:
    app = MyApp()
    app.run()

if __name__ == "__main__":
    main()

