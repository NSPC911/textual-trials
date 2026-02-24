from asyncio import sleep

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Static


class Application(App):
    def compose(self) -> ComposeResult:
        yield Static("Did you notice how fast the app loaded?")
        yield Static("That's because the on_mount method is a worker,")
        yield Static("so it doesn't block the app from loading while")
        yield Static("doing heavy things (like sleeping for 5 seconds).")

    @work
    async def on_mount(self) -> None:
        await sleep(5)


Application().run()
