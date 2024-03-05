from app import App as _App
from keyboard import key

class MyApp(_App):

    def _process(self) -> None:
        if self.kb.is_pressed(key.Q):
            self.request_quit()

def main() -> None:
    app = MyApp()
    app.run()

if __name__ == "__main__":
    main()

