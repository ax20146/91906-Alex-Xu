# /utils/classes/timer.py


from .clock import Clock


class Timer:
    __slots__ = "duration", "_clock", "_previous"

    def __init__(self, clock: Clock, duration: int) -> None:
        self.duration: int = duration
        self._clock: Clock = clock
        self._previous: float = clock.time

    def available(self) -> bool:
        return (
            False
            if self.duration < 0
            else self._clock.time - self._previous >= self.duration
        )

    def update(self) -> None:
        self._previous = self._clock.time
