import time
from collections.abc import Callable
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any

from textual.dom import DOMNode
from textual.message import Message


def throttle(delay: float) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Leading-edge throttle with trailing-edge debounce for Textual message handlers.

    The first event in a burst passes immediately. Events within `delay` seconds
    are blocked. The last blocked event fires after `delay * 1.1` seconds of silence.

    Returns:
        A decorator that wraps a Textual message handler (sync or async) with debounce logic.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        attr_last = f"_deb_last_{func.__name__}"
        attr_timer = f"_deb_timer_{func.__name__}"
        is_async = iscoroutinefunction(func)

        if is_async:
            @wraps(func)
            async def wrapper(self: DOMNode, event: Message, *args, **kwargs) -> None:
                now = time.monotonic()
                last_passed = getattr(self, attr_last, 0.0)
                trailing_timer = getattr(self, attr_timer, None)

                if now - last_passed >= delay:
                    if trailing_timer is not None:
                        trailing_timer.stop()
                        setattr(self, attr_timer, None)
                    setattr(self, attr_last, now)
                    await func(self, event, *args, **kwargs)
                else:
                    if trailing_timer is not None:
                        trailing_timer.stop()

                    captured = event

                    async def trailing() -> None:
                        setattr(self, attr_timer, None)
                        setattr(self, attr_last, time.monotonic())
                        await func(self, captured, *args, **kwargs)

                    setattr(self, attr_timer, self.set_timer(delay * 1.1, trailing))

            return wrapper
        else:
            @wraps(func)
            def wrapper(self: DOMNode, event: Message, *args, **kwargs) -> None:
                now = time.monotonic()
                last_passed = getattr(self, attr_last, 0.0)
                trailing_timer = getattr(self, attr_timer, None)

                if now - last_passed >= delay:
                    if trailing_timer is not None:
                        trailing_timer.stop()
                        setattr(self, attr_timer, None)
                    setattr(self, attr_last, now)
                    func(self, event, *args, **kwargs)
                else:
                    if trailing_timer is not None:
                        trailing_timer.stop()

                    captured = event

                    def trailing() -> None:
                        setattr(self, attr_timer, None)
                        setattr(self, attr_last, time.monotonic())
                        func(self, captured, *args, **kwargs)

                    setattr(self, attr_timer, self.set_timer(delay * 1.1, trailing))

            return wrapper

    return decorator
