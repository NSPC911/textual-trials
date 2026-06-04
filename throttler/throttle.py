import time
from collections.abc import Callable
from functools import wraps
from inspect import isawaitable, iscoroutinefunction
from typing import Any

from textual.dom import DOMNode
from textual.message import Message


def throttle(delay: float) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Leading-edge throttle with trailing-edge debounce for Textual message handlers.

    The first event in a burst passes immediately. Events within `delay` seconds
    are blocked. The last blocked event fires after `delay` seconds from the last allowed event.

    Returns:
        A decorator that wraps a Textual message handler (sync or async) with debounce logic.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        attr_last = f"_deb_last_{func.__name__}"
        attr_timer = f"_deb_timer_{func.__name__}"

        if iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(self: DOMNode, event: Message, *args, **kwargs) -> None:
                now = time.monotonic()
                last_passed = getattr(self, attr_last, 0.0)
                trailing_timer = getattr(self, attr_timer, None)

                if now - last_passed >= delay:
                    # run func
                    if trailing_timer is not None:
                        trailing_timer.stop()
                        setattr(self, attr_timer, None)
                    setattr(self, attr_last, now)
                    # not sure how workers are handled
                    obj = func(self, event, *args, **kwargs)
                    if isawaitable(obj):
                        await obj
                else:
                    if trailing_timer is not None:
                        trailing_timer.stop()

                    captured = event

                    async def trailing() -> None:
                        setattr(self, attr_timer, None)
                        setattr(self, attr_last, time.monotonic())
                        await func(self, captured, *args, **kwargs)

                    # Calculate remaining time until next allowed event
                    time_since_last = now - last_passed
                    remaining_delay = delay - time_since_last
                    setattr(self, attr_timer, self.set_timer(remaining_delay, trailing))

            return wrapper
        else:
            @wraps(func)
            def wrapper(self: DOMNode, event: Message, *args, **kwargs) -> None:
                now = time.monotonic()
                last_passed = getattr(self, attr_last, 0.0)
                trailing_timer = getattr(self, attr_timer, None)

                if now - last_passed >= delay:
                    # run func
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

                    # Calculate remaining time until next allowed event
                    time_since_last = now - last_passed
                    remaining_delay = delay - time_since_last
                    setattr(self, attr_timer, self.set_timer(remaining_delay, trailing))

            return wrapper

    return decorator
