from time import sleep

from textual.app import App, ComposeResult
from textual.widgets import Static


class Application(App):
    def compose(self) -> ComposeResult:
        yield Static("Did you notice the delay for the first paint?")
        yield Static("This is because of the sleep in on_mount.")

    def on_mount(self) -> None:
        sleep(5)


Application().run()
