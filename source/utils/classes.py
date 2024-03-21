TuplePoint = tuple[float, float]


class Clock:
    __slots__ = "time"

    def __init__(self) -> None:
        self.time: float = 0

    def update(self, dt: float) -> None:
        self.time += dt * 1000


class Timer:
    __slots__ = ("clock", "delay", "previous")

    def __init__(self, delay: int, clock: Clock) -> None:
        self.delay: int = delay
        self.clock: Clock = clock
        self.previous: float = clock.time

    def available(self) -> bool:
        return (
            self.clock.time - self.previous >= self.delay
            if self.delay > 0
            else False
        )

    def update(self) -> None:
        self.previous = self.clock.time


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x: float = x
        self.y: float = y

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Point):
            return NotImplemented

        return self.x == __value.x and self.y == __value.y

    def __gt__(self, __value: "Point") -> bool:
        return self.x > __value.x and self.y > __value.y

    def __lt__(self, __value: "Point") -> bool:
        return self.x < __value.x and self.y < __value.y

    def __add__(self, __value: "Point | float") -> "Point":
        if isinstance(__value, (int, float)):
            return self.__class__(self.x + __value, self.y + __value)

        return self.__class__(self.x + __value.x, self.y + __value.y)

    def __sub__(self, __value: "Point | float") -> "Point":
        if isinstance(__value, (int, float)):
            return self.__class__(self.x - __value, self.y - __value)

        return self.__class__(self.x - __value.x, self.y - __value.y)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def within(self, __value: "Point", /, *, range: int = 0) -> bool:
        return __value - range < self < __value + range

    def convert(self) -> TuplePoint:
        return (self.x, self.y)
