# /utils/classes.py


from abc import ABC, abstractmethod

import arcade

from .types import ClassVar, NamedTuple

__all__: list[str] = [
    "Clock",
    "Timer",
    "Point",
    "Vector",
    "Sprite",
]


class Clock:
    __slots__ = "_time"

    def __init__(self) -> None:
        self._time: float = 0

    @property
    def time(self) -> float:
        return self._time

    def update(self, delta_time: float) -> None:
        self._time += delta_time * 1000


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


class Point(NamedTuple):
    x: float
    y: float


class Vector:
    __slots__ = "x", "y"

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x: float = x
        self.y: float = y

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Vector):
            return NotImplemented

        return self.x == __value.x and self.y == __value.y

    def __lt__(self, __value: "Vector") -> bool:
        return self.x < __value.x and self.y < __value.y

    def __gt__(self, __value: "Vector") -> bool:
        return self.x > __value.x and self.y > __value.y

    def __add__(self, __value: "Vector | float") -> "Vector":
        if isinstance(__value, (int, float)):
            return self.__class__(self.x + __value, self.y + __value)

        return self.__class__(self.x + __value.x, self.y + __value.y)

    def __sub__(self, __value: "Vector | float") -> "Vector":
        if isinstance(__value, (int, float)):
            return self.__class__(self.x - __value, self.y - __value)

        return self.__class__(self.x - __value.x, self.y - __value.y)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def within(self, __value: "Vector", /, *, range: int = 0) -> bool:
        return __value - range < self < __value + range

    def convert(self) -> Point:
        return Point(self.x, self.y)


class Sprite(arcade.Sprite, ABC):
    clock: ClassVar[Clock]

    def __init__(
        self,
        filename: str,
        *,
        rotation: float = 0,
        position: Point = Point(0, 0),
    ) -> None:
        super().__init__(
            filename,
            angle=rotation,
            center_x=position.x,
            center_y=position.y,
        )

    @property
    def x(self) -> float:
        return self.center_x

    @x.setter
    def x(self, __value: float) -> None:
        self.center_x = __value

    @property
    def y(self) -> float:
        return self.center_y

    @y.setter
    def y(self, __value: float) -> None:
        self.center_y = __value

    @property
    def position(self) -> Point:  # type: ignore
        return Point(self.x, self.y)

    @abstractmethod
    def on_update(self, dt: float) -> None:  # type: ignore
        pass
