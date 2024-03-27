# /entities/enemies.py

from ..utils import Movement, Sprite, Vector
from ..utils.types import ClassVar


class Entity(Sprite):
    waypoints: ClassVar[tuple[Vector, ...]]

    FILENAME: str
    HEALTH: int
    SPEED: int

    def __init__(self) -> None:
        super().__init__(
            filename=self.FILENAME,
            position=self.waypoints[0],
        )

        self.target: int = 1
        self.health: int = self.HEALTH
        self.movement: Movement = Movement(
            self, self.SPEED, self.waypoints[self.target]
        )

    def is_end(self) -> bool:
        return self.target >= len(self.waypoints)

    def is_alive(self) -> bool:
        return self.health > 0

    def update(self) -> None:
        self.movement.move()
        self.movement.rotate()
        self.update_target()

    def update_target(self) -> None:
        if self.xy == self.waypoints[self.target]:
            self.target += 1

        if not self.is_end():
            self.movement.update_target(self.waypoints[self.target])
