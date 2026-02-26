from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import Button, Static


class Application(App):
    CSS = """
    HorizontalGroup#labels {
        height: 1fr;
    }
    HorizontalGroup#labels > Static {
        border: solid $accent;
        width: 1fr;
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        with VerticalGroup():
            with HorizontalGroup(id="labels"):
                yield Static("One")
                yield Static("Two", id="middle")
                yield Static("Three")
            with HorizontalGroup():
                yield Button("toggle middle one", id="toggle")
                yield Button("get middle one size", id="size")

    @on(Button.Pressed, "#toggle")
    def toggle_loading(self) -> None:
        middle = self.query_one("#middle", Static)
        middle.loading = not middle.loading

    @on(Button.Pressed, "#size")
    def toggle_size(self) -> None:
        middle = self.query_one("#middle", Static)
        self.notify(f"Middle size: {middle.size}")


Application().run()
