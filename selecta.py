from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Label, Footer, Header
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

PAGE_SIZE = 5

class FileItem(ListItem):
    def __init__(self, filename: str, **kwargs):
        super().__init__(**kwargs)
        self.filename = filename
        self.selected = False

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label(" ", id="checkbox", classes="checkbox"),
            Label(self.filename, classes="filename")
        )

    def set_selected(self, state: bool):
        self.selected = state
        self.query_one("#checkbox", Label).update("X" if state else " ")

class FileListView(ListView):
    BINDINGS = []

class FileListWidget(Vertical):
    DEFAULT_CSS = """
    FileListWidget {
        height: 100%;
    }
    FileListWidget > FileListView {
        height: 1fr;
    }
    FileListWidget > #widget-footer {
        display: none;
        background: $accent;
        color: $text;
        text-align: center;
        text-style: bold;
    }
    FileListWidget.selection-mode > #widget-footer {
        display: block;
    }
    FileListWidget .checkbox {
        display: none;
        width: 3;
        text-align: center;
    }
    FileListWidget.selection-mode .checkbox {
        display: block;
    }
    FileItem {
        height: 1;
        padding: 0;
    }
    FileItem > Horizontal {
        height: 1;
    }
    FileItem Label {
        height: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield FileListView(
            *[FileItem(f"file{i:02}.txt") for i in range(1, 40)],
            id="file-list"
        )
        yield Label("SELECTION", id="widget-footer")

    def get_items(self) -> list[FileItem]:
        return list(self.query_one("#file-list", FileListView).query(FileItem))

    def get_selected_count(self) -> int:
        return sum(1 for item in self.get_items() if item.selected)

    def manage_mode(self):
        if self.get_selected_count() > 0:
            self.add_class("selection-mode")
        else:
            self.remove_class("selection-mode")

    def toggle_at_cursor(self):
        lv = self.query_one("#file-list", FileListView)
        if lv.index is not None:
            items = self.get_items()
            items[lv.index].set_selected(not items[lv.index].selected)
        self.manage_mode()

    def step(self, direction: str) -> bool:
        """Toggle item at cursor, then move one step in direction.
        Returns True if cursor actually moved."""
        lv = self.query_one("#file-list", FileListView)
        items = self.get_items()
        if lv.index is None:
            return False
        items[lv.index].set_selected(not items[lv.index].selected)
        self.manage_mode()
        moved = False
        if direction == "up" and lv.index > 0:
            lv.index -= 1
            moved = True
        elif direction == "down" and lv.index < len(lv.children) - 1:
            lv.index += 1
            moved = True
        return moved

class FileListSelectionMock(App):
    BINDINGS = [
        Binding("s", "toggle_selection_mode", "Selection Mode"),
        Binding("space", "toggle_file", "Toggle File"),
        Binding("up", "move_up", "Up"),
        Binding("down", "move_down", "Down"),
        Binding("shift+up", "toggle_up", "Toggle Up"),
        Binding("shift+down", "toggle_down", "Toggle Down"),
        Binding("shift+pageup", "toggle_page_up", "Toggle PgUp"),
        Binding("shift+pagedown", "toggle_page_down", "Toggle PgDn"),
        Binding("shift+home", "toggle_home", "Toggle Home"),
        Binding("shift+end", "toggle_end", "Toggle End"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield FileListWidget()
        yield Footer()

    def action_toggle_selection_mode(self):
        widget = self.query_one(FileListWidget)
        widget.toggle_class("selection-mode")
        if not widget.has_class("selection-mode"):
            for item in widget.get_items():
                item.set_selected(False)

    def action_toggle_file(self):
        widget = self.query_one(FileListWidget)
        if not widget.has_class("selection-mode"):
            widget.add_class("selection-mode")
        widget.toggle_at_cursor()

    def action_move_up(self):
        widget = self.query_one(FileListWidget)
        lv = widget.query_one("#file-list", FileListView)
        if lv.index is not None and lv.index > 0:
            lv.index -= 1

    def action_move_down(self):
        widget = self.query_one(FileListWidget)
        lv = widget.query_one("#file-list", FileListView)
        if lv.index is not None and lv.index < len(lv.children) - 1:
            lv.index += 1

    def action_toggle_up(self):
        self.query_one(FileListWidget).step("up")

    def action_toggle_down(self):
        self.query_one(FileListWidget).step("down")

    def action_toggle_page_up(self):
        widget = self.query_one(FileListWidget)
        for _ in range(PAGE_SIZE):
            if not widget.step("up"):
                break

    def action_toggle_page_down(self):
        widget = self.query_one(FileListWidget)
        for _ in range(PAGE_SIZE):
            if not widget.step("down"):
                break

    def action_toggle_home(self):
        widget = self.query_one(FileListWidget)
        while widget.step("up"):
            pass

    def action_toggle_end(self):
        widget = self.query_one(FileListWidget)
        while widget.step("down"):
            pass

if __name__ == "__main__":
    FileListSelectionMock().run()