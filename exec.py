from textual.app import App, ComposeResult
from textual.widgets import TextArea, Button
from textual.containers import Container


class CodeExecutorApp(App):
    """A minimal app with a code textarea and execute button."""

    def compose(self) -> ComposeResult:
        yield Container(
            TextArea(id="code_editor", language="python"),
            Button("Execute", id="execute_btn"),
            id="main_container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "execute_btn":
            self.execute_code()

    def execute_code(self) -> None:
        code = self.query_one("#code_editor", TextArea).text

        try:
            # Execute the code
            exec(code)

            self.notify("Code executed successfully!", severity="information")
        except Exception as e:
            self.notify(f"Error: {e}", severity="error")


if __name__ == "__main__":
    app = CodeExecutorApp()
    app.run()
