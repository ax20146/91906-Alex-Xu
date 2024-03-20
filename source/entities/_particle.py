from abc import abstractmethod
from typing import Any

from ..utils import Sprite, Timer, TuplePoint


class Particle(Sprite):
    def __init__(
        self,
        filename: str,
        rotation: float,
        position: TuplePoint,
        *,
        delay: int = 0,
    ) -> None:
        super().__init__(
            filename,
            rotation=rotation,
            position=position,
        )
        if delay:
            self.timer: Timer = Timer(delay, self.clock)

        self.initialize()

    def on_update(self, dt: float, **kwargs: Any) -> None:
        if self.timer.available():
            self.timer.update()
            self.kill()

        self.update()

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError
