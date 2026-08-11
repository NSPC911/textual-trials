from __future__ import annotations

from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Header, RichLog

INSTRUCTIONS = """\
[u]Press some Mouse buttons![/]

To quit the app press [b]ctrl+q[/b] or press the Quit button below.\
"""


class KeysApp(App[None]):
    """Show key events in a text log."""

    TITLE = "Textual Keys"
    BINDINGS = [("c", "clear", "Clear")]
    CSS = """
    #buttons {
        dock: bottom;
        height: 3;
    }
    Button {
        width: 1fr;
    }
    """
    ENABLE_COMMAND_PALETTE = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog()
        yield Horizontal(
            Button("Clear", id="clear", variant="warning"),
            Button("Quit", id="quit", variant="error"),
            id="buttons",
        )

    def on_ready(self) -> None:
        self.query_one(RichLog).write(Panel(Text.from_markup(INSTRUCTIONS)), expand=True)

    def on_click(self, event: events.Click) -> None:
        self.query_one(RichLog).write(event)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.exit()
        elif event.button.id == "clear":
            self.query_one(RichLog).clear()


if __name__ == "__main__":
    KeysApp().run()
