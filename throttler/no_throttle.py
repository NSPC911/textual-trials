import datetime

from textual import events
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Footer, Label, RichLog


class MouseArea(Widget):
    DEFAULT_CSS = """
    MouseArea {
        height: 1fr;
        border: solid $warning;
        content-align: center middle;
    }
    """

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.app.query_one(RichLog).write(
            f"[dim]{ts}[/]  [yellow]MouseMove[/]  "
            f"x=[cyan]{event.x:3}[/]  y=[cyan]{event.y:3}[/]"
        )


class Apple(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    RichLog {
        height: 1fr;
        border: solid $primary;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Move your mouse in the area below - events not debounced")
        yield MouseArea()
        yield RichLog(highlight=True, markup=True)
        yield Footer()


if __name__ == "__main__":
    Apple().run()
