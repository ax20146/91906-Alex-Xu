# /utils/classes/timer.py


# Import Local Dependencies
from .clock import Clock


# Define Timer Class
class Timer:
    __slots__ = "delay", "_clock", "_previous"

    def __init__(self, clock: Clock, delay: int) -> None:
        self.delay: int = delay
        self._clock: Clock = clock
        self._previous: float = clock.time

    def available(self) -> bool:
        return (
            self._clock.time - self._previous >= self.delay
            if self.delay > 0
            else False
        )

    def update(self) -> None:
        self._previous = self._clock.time
