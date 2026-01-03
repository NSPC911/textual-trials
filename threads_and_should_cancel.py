from asyncio import sleep

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Button, RichLog
from textual.worker import NoActiveWorker, WorkerCancelled, get_current_worker


def should_cancel() -> bool:
    """
    Whether the current worker should cancel execution

    Returns:
        bool: whether to cancel this worker or not
    """
    try:
        worker = get_current_worker()
    except RuntimeError:
        return False
    except WorkerCancelled:
        return True
    except NoActiveWorker:
        return False
    return bool(worker and not worker.is_running)


class Application(App):
    def compose(self) -> ComposeResult:
        self.richlog = RichLog()
        yield self.richlog
        with HorizontalGroup():
            yield Button("Run worker", id="worker")
            yield Button("Run worker THREAD", id="thread")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.richlog.write(event.button.id)

    @on(Button.Pressed, "#worker")
    @work(exclusive=True, thread=False)
    async def worker_runner(self, event: Button.Pressed) -> None:
        await sleep(1)  # simulate process intensive thing
        self.richlog.write("Worker completed!")

    @on(Button.Pressed, "#thread")
    @work(exclusive=True, thread=True)
    def thread_runner(self, event: Button.Pressed) -> None:
        self.call_from_thread(sleep, 1)
        self.richlog.write("Checking should_cancel...")
        if should_cancel():
            self.richlog.write("Thread was supposedly cancelled!")
        self.call_from_thread(sleep, 1)
        self.richlog.write("Thread completed!")


Application().run()
