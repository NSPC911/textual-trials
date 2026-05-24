from textual.app import App


class ThemeTestApp(App):
    CSS_PATH = "panel-broken.tcss"


ThemeTestApp().run()
