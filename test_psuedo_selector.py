from textual.app import App, ComposeResult
from textual.dom import DOMNode
from textual.widgets import Button, RichLog


class Application(App):
    def compose(self) -> ComposeResult:
        yield Button()
        self.richlog = RichLog()
        yield self.richlog

    def doaquery(self, selector: str) -> DOMNode | None:
        try:
            return self.query_one(selector)
        except Exception:
            return None

    def on_mount(self) -> None:
        self.set_interval(1, lambda: self.richlog.write(f"Button query returned = {self.doaquery('*:focus')}"))

Application().run()
