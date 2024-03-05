from app import App as _App
from editor import Editor
from util import ASSERT

from stages import Stage
from stages import MainMenu
from stages import TodoStage
from stages import PasswordManager
from stages import TankeStelle

class MyApp(_App):

    def __init__(self) -> None:
        super().__init__()

        self.editor: Editor = Editor(self.kb)

        class _stages:
            mainmenu = MainMenu(self)
            todo = TodoStage(self)
            passmgr = PasswordManager(self)
            tanke = TankeStelle(self)

        self._stages = _stages
        self._stage: Stage = self._stages.mainmenu

    def request_quit(self) -> None:
        self._stage.exit()
        super().request_quit()

    def switch_stage(self, new_stage: str) -> None:
        stage = {"mainmenu": self._stages.mainmenu,
                 "todo": self._stages.todo,
                 "passmgr": self._stages.passmgr,
                 "tanke": self._stages.tanke}.get(new_stage)
        self._stage.exit()
        ASSERT(isinstance(stage, Stage), f"Unknown stage name '{new_stage}'")
        self._stage = stage
        self._stage.process()

    def _process(self) -> None:
        self._stage.process()
        self.editor.process()

        # Consume all the other button press events
        if not self.editor.is_active():
            self.kb.clear()

    def _render(self) -> None:
        self._stage.render()
        self.editor.render(self.screen)
        super()._render()

def main():
    app = MyApp()
    app.run()

if __name__ == "__main__":
    main()

