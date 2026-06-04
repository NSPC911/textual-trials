import datetime

from textual import events
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Footer, Label, RichLog

from throttle import throttle

THROTTLE_DELAY = 0.1


class MouseArea(Widget):
    DEFAULT_CSS = """
    MouseArea {
        height: 1fr;
        border: solid $warning;
        content-align: center middle;
    }
    """

    @throttle(THROTTLE_DELAY)
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
        yield Label(
            f"move your mouse in the area below - events debounced to {THROTTLE_DELAY * 1000:.0f} ms "
        )
        yield MouseArea()
        yield RichLog(highlight=True, markup=True)
        yield Footer()


if __name__ == "__main__":
    Apple().run()
