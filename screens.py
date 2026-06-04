from textual.app import App
from textual.events import Key
from textual.screen import Screen
from textual.widgets import Placeholder


class MyScreen(Screen):
    def compose(self):
        yield Placeholder()

    def on_key(self, event: Key) -> None:
        self.notify(f"On screen: {event.key}")
        return


class TestApp(App):
    def on_mount(self):
        self.push_screen(MyScreen())

    def on_key(self, event: Key) -> None:
        self.notify(f"On app: {event.key}")


if __name__ == "__main__":
    TestApp().run()
