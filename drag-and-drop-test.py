from textual.app import App, ComposeResult
from textual.events import Paste
from textual.widgets import Static


class DNDApp(App):
    def compose(self) -> ComposeResult:
        yield Static("Try dropping something on my head!")
        yield Static("Make sure that this terminal is not privileged, otherwise drag and drop won't work.")


    def on_paste(self, event: Paste) -> None:
        self.notify(f"Got paste event with data: {event!r}")


DNDApp().run()
