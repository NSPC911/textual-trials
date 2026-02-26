from textual.app import App
from textual.containers import Grid
from textual.widgets import Label


class AllBordersApp(App):
    DEFAULT_CSS = """
    #ascii { border: ascii $accent }
    #blank { border: blank $accent }
    #dashed { border: dashed $accent }
    #double { border: double $accent }
    #heavy { border: heavy $accent }
    #hidden { border: hidden $accent }
    #hkey { border: hkey $accent }
    #inner { border: inner $accent }
    #outer { border: outer $accent }
    #panel { border: panel $accent }
    #round { border: round $accent }
    #solid { border: solid $accent }
    #tall { border: tall $accent }
    #thick { border: thick $accent }
    #vkey { border: vkey $accent }
    #wide { border: wide $accent }
    Grid {
        grid-size: 4 4;
        align: center middle;
        grid-gutter: 1 2;
    }
    Label {
        width: 20;
        height: 3;
        content-align: center middle;
        background: green
    }
    """

    def compose(self):
        yield Grid(
            Label("ascii", id="ascii"),
            Label("blank", id="blank"),
            Label("dashed", id="dashed"),
            Label("double", id="double"),
            Label("heavy", id="heavy"),
            Label("hidden/none", id="hidden"),
            Label("hkey", id="hkey"),
            Label("inner", id="inner"),
            Label("outer", id="outer"),
            Label("panel", id="panel"),
            Label("round", id="round"),
            Label("solid", id="solid"),
            Label("tall", id="tall"),
            Label("thick", id="thick"),
            Label("vkey", id="vkey"),
            Label("wide", id="wide"),
        )


if __name__ == "__main__":
    app = AllBordersApp()
    app.run()
