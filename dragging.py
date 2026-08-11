import contextlib
from random import randint

from textual import events, on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.css.query import NoMatches
from textual.widgets import SelectionList, Static
from textual.widgets.selection_list import Selection


def randid() -> str:
    return f"id_{randint(0, 1000000)}"


class Application(App):
    DEFAULT_CSS = """
    #playlist,
    Container {
        width: 1fr;
        height: 1fr;
        border: round $accent;
        background: transparent
    }
    Horizontal {
        height: 1fr;
    }
    #popup {
        layer: overlay;
        width: auto;
        border: round $accent
    }
    """

    was_mouse_down_on_playlist: bool = False
    songs_to_drop: list[str] = []

    def compose(self) -> ComposeResult:
        with Horizontal(id="root"):
            yield SelectionList(
                # thanks autocomplete, lysm (i dont actually listen to these songs btw)
                Selection(
                    "Blinding Lights - The Weeknd", id=randid(), value="blinding_lights"
                ),
                Selection(
                    "Shape of You - Ed Sheeran", id=randid(), value="shape_of_you"
                ),
                Selection("Levitating - Dua Lipa", id=randid(), value="levitating"),
                Selection("Bad Guy - Billie Eilish", id=randid(), value="bad_guy"),
                Selection(
                    "Uptown Funk - Mark Ronson ft. Bruno Mars",
                    id=randid(),
                    value="uptown_funk",
                ),
                Selection("Senorita - Shawn Mendes & Camila Cabello", id=randid(), value="senorita"),
                Selection("Old Town Road - Lil Nas X", id=randid(), value="old_town_road"),
                Selection("Havana - Camila Cabello ft. Young Thug", id=randid(), value="havana"),
                Selection("Rockstar - Post Malone ft. 21 Savage", id=randid(), value="rockstar"),
                Selection("Closer - The Chainsmokers ft. Halsey", id=randid(), value="closer"),
                Selection("Sunflower - Post Malone & Swae Lee", id=randid(), value="sunflower"),
                Selection("Animals - Martin Garrix", id=randid(), value="animals"),
                id="playlist",
            )
            yield Container(Static("drag here!!"), id="recipient")

    @on(events.MouseDown)
    def on_mouse_down_on_playlist(self, event: events.MouseDown) -> None:
        if (
            (self.screen.get_widget_at(event.screen_x, event.screen_y)[0]).id
            == "playlist"
        ):
            self.was_mouse_down_on_playlist = True

    @on(events.MouseUp)
    @work
    async def on_mouse_up_on_anything(self, event: events.MouseUp) -> None:
        self.was_mouse_down_on_playlist = False
        with contextlib.suppress(NoMatches):
            await self.query_one("#popup", Static).remove()
        # forced to do this, because popup doesn't actually get removed asap, im not sure why
        self.call_after_refresh(self.handle_drop, event)

    def handle_drop(self, event: events.MouseUp) -> None:
        if self.screen.get_widget_at(event.screen_x, event.screen_y)[0].id == "recipient":
            self.query_one("#recipient > Static", Static).update(
                f"{len(self.query_one('#playlist').selected)} songs",
            )
        # you can do stuff with self.songs_to_drop here, its just there for what you want to do

    @on(events.MouseMove)
    @work
    async def on_mouse_move(self, event: events.MouseMove) -> None:
        if self.was_mouse_down_on_playlist:
            if not self.query("#popup"):
                playlist = self.query_one("#playlist", SelectionList)
                if len(songs := playlist.selected) < 1:
                    return
                await self.mount(
                    popup := Static(f"{len(songs)} songs", id="popup")
                )
                self.songs_to_drop = songs
            else:
                popup = self.query_one("#popup", Static)
            popup.offset = (event.screen_x, event.screen_y)


Application().run()
