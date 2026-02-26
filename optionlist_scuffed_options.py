from textual.app import App, ComposeResult
from textual.widgets import OptionList
from textual.widgets.option_list import Option


class Application(App):
    def compose(self) -> ComposeResult:
        yield OptionList(
            Option("Option 1"),
            Option("Option 2"),
            Option("Option 3"),
            Option("𝙊𝙋𝙏𝙄𝙊𝙉 𝟰"),
            Option("Option 5"),
            Option("Option 6"),
            Option("Option 7"),
        )


Application().run()
