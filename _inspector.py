from typing import cast
from rich.text import TextType
from textual import events, on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.css.query import NoMatches, QueryType
from textual.dom import BadIdentifier, DOMNode, check_identifiers
from textual.validation import ValidationResult, Validator
from textual.widgets import Input, Label, TabbedContent, TextArea, Tree
from textual.widgets.tree import TreeDataType, TreeNode

from resizebar import HorizontalResizeBar, VerticalResizeBar


class CheckID(Validator):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, value: str) -> ValidationResult:
        try:
            check_identifiers("id", value)
            return self.success()
        except BadIdentifier as exc:
            return self.failure(str(exc))


class DOMTree(Tree):
    DEFAULT_CSS = """
    DOMTree {
        background: transparent;
        height: 1fr
    }
    """

    def __init__(
        self,
        label: TextType,
        data: TreeDataType | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            label, data, name=name, id=id, classes=classes, disabled=disabled
        )
        self.prev_hovered_index = -1


class Inspector(HorizontalGroup):
    DEFAULT_CSS = """
    Inspector {
        dock: right;
        width: 0.25fr;
        &.-hide {
            width: 0;
        }
        #tabcontentwrapper {
            height: 0.5fr
        }
        #css {
            Input {
                border: none !important;
                height: 1;
                padding: 0;
                scrollbar-size: 0 0 !important;
                overflow: hidden hidden;
                width: 1fr;
                background: transparent !important
            }
            Static {
                width: auto;
                text-wrap: nowrap;
                text-overflow: ellipsis;
            }
            Static#filler {
                width: 2;
                text-overflow: clip;
            }
        }
        #id, #classes {
            Label {
                height: 3;
                padding: 1;
                width: 9;
                text-align: center;
                .input--placeholder {
                    color: $foreground-darken-1
                }
            }
            Input {
                width: 1fr;
            }
        }
        &:focus HorizontalResizeBar,
        &:focus-within HorizontalResizeBar {
            border-left: outer $border
        }
        &:focus VerticalResizeBar,
        &:focus-within VerticalResizeBar {
            border-top: outer $border
        }
    }
    """

    def __init__(self) -> None:
        super().__init__(classes="-hide")
        self.visible = False
        self.forced_width = None

    def compose(self) -> ComposeResult:
        yield HorizontalResizeBar(self)
        with VerticalGroup():
            tree = DOMTree("Application")
            tree.guide_depth = 1
            yield tree
            tabarea = VerticalGroup(id="tabcontentwrapper")
            with tabarea:
                yield VerticalResizeBar(tabarea)
                with TabbedContent("CSS", "ID & Classes"):
                    with VerticalGroup(id="css"):
                        yield TextArea(
                            language="css",
                            read_only=True,
                            soft_wrap=False,
                            show_line_numbers=True,
                            compact=True,
                            placeholder="No TCSS available",
                        )
                    with VerticalScroll(id="idandclasses"):
                        with HorizontalGroup(id="id"):
                            yield Label("ID")
                            yield Input(
                                placeholder="No IDs",
                                validators=[CheckID()],
                                validate_on=["changed"],  # ty: ignore[invalid-argument-type]
                                valid_empty=True,
                            )
                        with HorizontalGroup(id="classes"):
                            yield Label("Classes")
                            yield Input(
                                placeholder="No Classes",
                                validate_on=["changed"],  # ty: ignore[invalid-argument-type]
                                valid_empty=True,
                            )

    def on_mount(self) -> None:
        self.app.DEFAULT_CSS += """
/* .-highlight *, */
.-highlight {
  /* hatch: "╲" skyblue !important; */
  background: $accent 50% !important;
}
"""

    def has_child(self, child: type[QueryType] | str | None = None) -> bool:
        if child is None:
            return len(self.query()) > 0
        try:
            self.query_one(child)
            return True
        except NoMatches:
            return False

    def action_toggle_devtools_inspector(self) -> None:
        self.display = not self.display

    @on(events.Hide)
    def on_hide(self, _: events.Hide | None = None) -> None:
        self.forced_width = self.styles.width
        self.styles.width = 0
        self.add_class("-hide")

    async def make_tree(self) -> DOMTree:
        try:
            tree: DOMTree = self.query_one(DOMTree)
        except NoMatches:
            tree = DOMTree("Application")
            await self.mount(tree)
        tree: DOMTree = tree.clear()

        def build_textual_tree(parent_node: TreeNode, dom_node: DOMNode) -> None:
            for child in dom_node.query_children("*"):
                if child is self:
                    continue
                node_type = type(child).__name__
                label = f"[bold]{node_type}[/bold]"
                if child.id:
                    label += f' [cyan]id="{child.id}"[/cyan]'
                if child.classes:
                    label += f' [green]class="{" ".join(child.classes)}"[/green]'
                if not child.query_children("*"):
                    parent_node.add_leaf(label, data=child)
                else:
                    child_tree_node = parent_node.add(label, data=child)
                    build_textual_tree(child_tree_node, child)

        build_textual_tree(tree.root, self.app)
        return tree

    @on(events.Show)
    async def on_show(self, _: events.Show | None = None) -> None:
        self.remove_class("-hide")
        tree = await self.make_tree()
        tree.focus()
        tree.action_toggle_expand_all()
        tree.action_toggle_expand_all()
        tree.action_toggle_expand_all()
        self.styles.width = self.forced_width

    @on(DOMTree.NodeHighlighted)
    async def on_tree_node_highlighted(self, event: DOMTree.NodeHighlighted) -> None:
        if isinstance(event.node.data, DOMNode):
            # first id and classes
            if event.node.data.id is None:
                self.query_one("#id > Input", Input).value = ""
            else:
                self.query_one("#id > Input", Input).value = event.node.data.id
            if event.node.data.id is None:
                self.query_one("#classes > Input", Input).value = ""
            else:
                self.query_one("#classes > Input", Input).value = " ".join(
                    event.node.data.classes
                )
            # then css dump
            self.query_one("#css > TextArea", TextArea).load_text(
                event.node.data.styles.base.css
            )

    @on(Input.Changed, "#id > Input")
    @on(Input.Changed, "#classes > Input")
    def update_class_or_id(self, event: Input.Changed) -> None:
        assert event.input.parent is not None
        domtree: DOMTree = self.query_one(DOMTree)
        if domtree.cursor_node is None or not event.input.is_valid:
            return
        if not isinstance(domtree.cursor_node.data, DOMNode):
            return
        if event.input.parent.id == "id":
            domtree.cursor_node.data._nodes.updated()
            domtree.cursor_node.data._id = event.value
        elif event.input.parent.id == "classes":
            domtree.cursor_node.data.classes = frozenset(event.value.split())

    @on(events.MouseMove)
    async def on_mouse_move(self, event: events.MouseMove) -> None:
        if isinstance(event.widget, DOMTree) and event.widget.hover_line != -1:
            node = event.widget.get_node_at_line(event.widget.hover_line)
            if node is not None and isinstance(node.data, DOMNode):
                async with self.batch():
                    if event.widget.prev_hovered_index != -1:
                        prev_hovered_node = event.widget.get_node_at_line(
                            event.widget.prev_hovered_index
                        )
                        if prev_hovered_node is not None and isinstance(
                            prev_hovered_node.data, DOMNode
                        ):
                            if prev_hovered_node.data is node.data:
                                return
                            prev_hovered_node.data.remove_class("-highlight")
                    node.data.add_class("-highlight")
                    event.widget.prev_hovered_index = event.widget.hover_line

    @on(events.Leave)
    def on_mouse_leave(self, event: events.Leave) -> None:
        domtree: DOMTree = self.query_one(DOMTree)
        if domtree.prev_hovered_index != -1 and hasattr(
            node := domtree.get_node_at_line(domtree.prev_hovered_index), "data"
        ):
            cast(DOMNode, node.data).remove_class("-highlight")
