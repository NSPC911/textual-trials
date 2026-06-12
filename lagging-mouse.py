"""MRE: one comma-grouped rule with a `:hover` variant makes EVERY widget hover-styled.

Textual computes `widget._has_hover_style` from a cheap name index, not real
selector matching (stylesheet.py, `Stylesheet.apply`):

1. `RuleSet._post_parse` unions pseudo-classes across ALL comma variants of a
   rule group, so `Button:hover` taints the whole group with "hover".
2. A rule group is a candidate for a widget if the FINAL selector name of ANY
   variant intersects the widget's names. `#footer > *` is indexed under `*`,
   which intersects every widget.

Combined: every widget in the app gets `_has_hover_style = True`, even though
the `:hover` declarations can only ever match Buttons inside #footer.

A hover-flagged widget pays `update_node_styles()` — a full stylesheet
re-application over itself and its children — TWICE per MouseMove, even when
the widget under the mouse did not change (`App._set_mouse_over` has no
identity guard). With a realistically sized stylesheet this floods the message
queue; in fast-reporting terminals (kitty) the app visibly freezes while the
mouse moves.

Reproduce:
    python lagging-mouse.py
    Move the mouse around the OptionList and watch the counter climb.
    Set GROUPED = False (same declarations, :hover split into its own rule)
    and the counter stays at zero.
"""

import time

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.css.query import NoMatches
from textual.dom import DOMNode
from textual.widgets import Button, Label, OptionList

GROUPED = True  # False = identical styling, :hover in its own rule block
BULK_RULES = 1000  # simulates a real app's stylesheet size (rovr has ~1000+ rules)

HOVER_CSS_GROUPED = """
    #footer > *,
    Button:hover {
        border: solid green;
    }
"""

HOVER_CSS_SPLIT = """
    #footer > * {
        border: solid green;
    }
    Button:hover {
        border: solid green;
    }
"""

# Candidate rules for OptionList that never match (no .bulk-N ancestor exists).
# Each style re-application must still consider all of them, once per
# component class — this is the cost multiplier, not the cause.
BULK_CSS = "\n".join(
    f".bulk-{n} OptionList {{ color: red; }}" for n in range(BULK_RULES)
)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MRE for Textual hover style performance issue")
    parser.add_argument("--split", action="store_true", help="Use split CSS rules instead of grouped")
    if (args := parser.parse_args()).split:
        GROUPED = False


class LaggingMouseApp(App):
    CSS = f"""
    OptionList {{ height: 1fr; }}
    #footer {{ height: 3; dock: bottom; }}
    #status {{ width: 1fr; content-align: right middle; }}
    {HOVER_CSS_GROUPED if GROUPED else HOVER_CSS_SPLIT}
    {BULK_CSS}
    """

    def compose(self) -> ComposeResult:
        yield OptionList(*(f"option {n}" for n in range(100)))
        with Horizontal(id="footer"):
            yield Button("a button")
            yield Label(id="status")

    def on_mount(self) -> None:
        self.restyles = 0
        self.restyle_seconds = 0.0
        self.counting = False
        original = DOMNode.update_node_styles
        app = self

        def counted(node: DOMNode, animate: bool = True) -> None:
            start = time.perf_counter()
            original(node, animate=animate)
            if app.counting:
                app.restyle_seconds += time.perf_counter() - start
                app.restyles += 1
                app.show_status()

        DOMNode.update_node_styles = counted

    def on_ready(self) -> None:
        self.counting = True
        self.show_status()

    def show_status(self) -> None:
        try:
            option_list = self.query_one(OptionList)
        except NoMatches:
            return
        avg_ms = self.restyle_seconds / self.restyles * 1000 if self.restyles else 0.0
        self.query_one("#status", Label).update(
            f"GROUPED={GROUPED} | "
            f"OptionList._has_hover_style={option_list._has_hover_style} | "
            f"restyles: {self.restyles} ({avg_ms:.2f} ms avg)"
        )


if __name__ == "__main__":
    LaggingMouseApp().run()


"""
Fix for this issue is to monkey patch the App class

    def _set_mouse_over(
        self, widget: Widget | None, hover_widget: Widget | None
    ) -> None:
        # Textual re-applies hover styles twice per MouseMove even when the
        # hovered widget hasn't changed, which floods the message queue when a
        # custom stylesheet marks large containers as hover-styled
        if widget is self.mouse_over and hover_widget is self.hover_over:
            return
        super()._set_mouse_over(widget, hover_widget)
"""
