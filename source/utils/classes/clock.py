# /utils/classes/clock.py


class Clock:
    __slots__ = "_time"

    def __init__(self) -> None:
        self._time: float = 0

    @property
    def time(self) -> float:
        return self._time

    def update(self, delta_time: float) -> None:
        self._time += delta_time * 1000
