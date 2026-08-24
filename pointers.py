from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.css.types import PointerShape
from textual.widgets import Static

POINTERS: list[PointerShape] = [
    "default",
    "pointer",
    "text",
    "crosshair",
    "help",
    "wait",
    "progress",
    "move",
    "grab",
    "grabbing",
    "cell",
    "vertical-text",
    "alias",
    "copy",
    "no-drop",
    "not-allowed",
    "n-resize",
    "s-resize",
    "e-resize",
    "w-resize",
    "ne-resize",
    "nw-resize",
    "se-resize",
    "sw-resize",
    "ew-resize",
    "ns-resize",
    "nesw-resize",
    "nwse-resize",
    "zoom-in",
    "zoom-out",
]


class PointerCell(Static):
    ALLOW_SELECT = False

    def __init__(self, pointer_name: PointerShape) -> None:
        super().__init__(pointer_name)
        self.pointer_name = pointer_name
        self.styles.pointer = pointer_name


class PointersApp(App):
    CSS = """
    Grid {
        grid-size: 5 6;
        grid-gutter: 1;
    }
    PointerCell {
        content-align: center middle;
        background: $panel;
        border: round $primary;
        width: 1fr;
        height: 1fr;
    }
    PointerCell:hover {
        background: $boost;
    }
    """

    def compose(self) -> ComposeResult:
        yield Grid(*(PointerCell(name) for name in POINTERS))


if __name__ == "__main__":
    PointersApp().run()
