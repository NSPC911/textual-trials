from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, SelectionList
from textual.widgets.selection_list import Selection


class Application(App):
    opt_count = 10

    def compose(self) -> ComposeResult:
        yield Button("remake options", id="remake")
        yield Button("list selected", id="list")
        yield SelectionList(
            *(Selection(f"opt {i}", value=f"opt {i}", id=f"opt_{i}") for i in range(10))
        )

    @on(Button.Pressed, "#remake")
    def remake_opts(self) -> None:
        self.query_one(SelectionList).set_options(
            Selection(
                f"opt {i + self.opt_count}",
                value=f"opt {i + self.opt_count}",
                id=f"opt_{i + self.opt_count}",
            )
            for i in range(10)
        )
        self.opt_count += 10

    @on(Button.Pressed, "#list")
    def list_repr_selected(self) -> None:
        self.notify(str(self.query_one(SelectionList).selected))


Application().run()
