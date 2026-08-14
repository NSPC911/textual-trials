# /// script
# dependencies = [
#     "faker",
#     "rich>=15.0.0",
#     "textual>=8.2.8",
# ]
# ///

import faker
from rich.segment import Segment
from rich.style import Style
from textual.app import App, ComposeResult
from textual.geometry import Region
from textual.strip import Strip
from textual.widgets import Footer, OptionList, SelectionList
from textual.widgets.selection_list import Selection


class BorderSelectionList(SelectionList[None]):
    """A SelectionList that shows selected options on its left border."""

    MARKER_STYLE = Style(color="yellow", bgcolor="yellow")

    def _get_left_gutter_width(self) -> int:
        return 0

    def render_line(self, y: int) -> Strip:
        # Skip SelectionList's checkbox while retaining OptionList highlighting.
        return OptionList.render_line(self, y)

    def render_lines(self, crop: Region) -> list[Strip]:
        lines = super().render_lines(crop)
        if crop.x != 0:
            return lines

        selected = set(self.selected)
        content_top = self.styles.gutter.top
        for output_y, widget_y in enumerate(crop.line_range):
            content_y = widget_y - content_top
            option_index = self.scroll_offset.y + content_y
            if (
                0 <= content_y < self.scrollable_content_region.height
                and 0 <= option_index < self.option_count
                and self.get_option_at_index(option_index).value in selected
            ):
                lines[output_y] = Strip.join((
                    Strip([Segment(" ", self.MARKER_STYLE)], 1),
                    lines[output_y].crop(1),
                ))
        return lines


class BorderSelectionApp(App[None]):
    CSS = """
    Screen {
        align: center middle;
    }

    BorderSelectionList {
        width: 32;
        height: 16;
        border: tall $border;
    }
    """

    def compose(self) -> ComposeResult:
        yield BorderSelectionList().set_options(Selection(name := faker.Faker().name(), value=name) for _ in range(20))
        yield Footer()


if __name__ == "__main__":
    BorderSelectionApp().run()
