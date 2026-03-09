from rich.markup import escape
from textual.app import App, ComposeResult
from textual.widgets import Button

target_desc = "[blink]This[/] is a [b]notification[/] with [i]markup[/]."
target_title = "Notification with {}"


class Application(App):
    def compose(self) -> ComposeResult:
        yield Button("Notify with markup", id="notify-markup")
        yield Button("Notify with markup disabled", id="notify-markup-disabled")
        yield Button("Notify with markup, but escaped", id="notify-markup-escaped")
        yield Button("Notify with markup, but escaped and disabled", id="notify-markup-escaped-disabled")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "notify-markup":
                self.notify(target_desc, title=target_title.format("markup"))
            case "notify-markup-disabled":
                self.notify(target_desc, title=target_title.format("no markup"), markup=False)
            case "notify-markup-escaped":
                self.notify(escape(target_desc), title=escape(target_title.format("escaped markup")), markup=True)
            case "notify-markup-escaped-disabled":
                self.notify(escape(target_desc), title=escape(target_title.format("escaped no markup")), markup=False)


Application().run()
