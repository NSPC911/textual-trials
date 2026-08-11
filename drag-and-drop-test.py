import shlex
from os import path
from sys import platform

from textual.app import App, ComposeResult
from textual.events import Paste
from textual.widgets import Static


class DNDApp(App):
    def compose(self) -> ComposeResult:
        yield Static("Try dropping something on my head!")
        yield Static("Make sure that this terminal is not privileged, otherwise drag and drop won't work.")

    def on_paste(self, event: Paste) -> None:
        self.notify(f"Got paste event with data: {event!r}")
        # attempt to parse it
        # first check if it is a full file path
        event.text = event.text.strip()
        if path.exists(event.text):
            self.notify(f"Parsed data: {event.text!r} (file path)")
        # otherwise, try to parse it as a list of arguments
        else:
            splitted = shlex.split(event.text, posix=platform != "win32")
            for i in range(len(splitted)):
                splitted[i] = splitted[i].strip().strip('"').strip("'")
            self.notify(f"Parsed data: {splitted!r} (arguments)")


DNDApp().run()
