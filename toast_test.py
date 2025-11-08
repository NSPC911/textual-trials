from textual.app import App, ComposeResult
from textual.widgets import Button


class Application(App):
    def compose(self) -> ComposeResult:
        yield Button("Start Information", variant="success", id="information")
        yield Button("Start Warning", variant="warning", id="warning")
        yield Button("Start Error", variant="error", id="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.notify(f"Button with id {event.button.id} was pressed!", severity=event.button.id)

Application().run()
