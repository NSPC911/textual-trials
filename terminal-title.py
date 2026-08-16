from textual.app import App, ComposeResult
from textual.widgets import Button, Input


class TerminalTitleApp(App):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter terminal title...")
        yield Button("Set Title", id="set_title_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.title = self.query_one(Input).value

    def watch_title(self, title: str) -> None:
        try:
            self._driver.write(f"\x1b]0;{title}\x07")
            self._driver.flush()
        except AttributeError:
            # driver not yet initialised
            pass


TerminalTitleApp().run()
