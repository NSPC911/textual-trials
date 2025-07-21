import asyncio
from random import randint

from textual import on, events, work
from textual.app import App, ComposeResult
from textual.containers import Grid, Container
from textual.screen import ModalScreen
from textual.widgets import Button, Label, ProgressBar

class Dismissable(ModalScreen):
    """Super simple screen that can be dismissed."""

    DEFAULT_CSS = """
    Dismissable {
        align: center middle
    }
    #dialog {
        grid-size: 1;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 1 3;
        width: 50vw;
        max-height: 13;
        border: round $primary-lighten-3;
        column-span: 3
    }
    #message {
        height: 1fr;
        width: 1fr;
        content-align: center middle
    }
    Container {
        align: center middle
    }
    Button {
        width: 50%
    }
    """

    def __init__(self, message: str, **kwargs):
        super().__init__(**kwargs)
        self.message = message

    def compose(self) -> ComposeResult:
        with Grid(id="dialog"):
            yield Label(self.message, id="message")
            with Container():
                yield Button("Ok", variant="primary", id="ok")

    def on_mount(self) -> None:
        self.query_one("#ok").focus()

    @on(Button.Pressed, "#ok")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        self.dismiss()

class TestApp(App):
    def compose(self) -> None:
        yield Container()
        yield Button("test", id="test")
    @on(Button.Pressed, "#test")
    @work(thread=True)
    def if_button_pressed(self, event: Button.Pressed) -> None:
        progress = ProgressBar(total=randint(1,50))
        self.call_from_thread(self.mount, progress)
        while progress.percentage != 1:
            self.call_from_thread(progress.advance)
            self.call_from_thread(asyncio.sleep, 0.5)
            if randint(1,3) == 1:
                self.call_from_thread(self.push_screen_wait, Dismissable("hi"))

TestApp().run()
