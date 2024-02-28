from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import App
    from handler import Handler
    from ui import Layout
    from keyboard import Keyboard
    from screen import Screen
    from editor import Editor

class Stage:

    def __init__(self, app: App) -> None:
        self.app = app
        self.editor: Editor = self.app.editor
        self.screen: Screen = self.app.screen
        self.kb: Keyboard = self.app.kb
        self.handler: Handler
        self.layout: Layout

    def render(self) -> None:
        pass

    def process(self) -> None:
        pass

    def exit(self) -> None:
        pass

