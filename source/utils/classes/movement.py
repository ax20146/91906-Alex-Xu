# /utils/classes/movement.py


from .sprite import Sprite
from .vector import Vector


class Movement:
    __slots__ = "_sprite", "_speed", "_target"

    def __init__(
        self, sprite: Sprite, speed: int, target: Vector | None = None
    ) -> None:
        self._sprite: Sprite = sprite
        self._speed: int = speed
        self._target: Vector | None = target

    def move(self, delta_time: float) -> None:
        if not self._target:
            raise ValueError("Invalid target 'None'")

        movement: Vector = self._target - self._sprite.position

        if movement.length() < self._speed * delta_time:
            self._sprite.position_update(movement)
            return

        self._sprite.position_update(
            movement.normalise() * self._speed * delta_time
        )

    def update_target(self, target: Vector) -> None:
        self._target = target
