import arcade

from ..utils.types import ClassVar, final
from .enemies import Enemy
from .entity import Entity


class Reinforcement(Entity):
    targets: ClassVar[arcade.SpriteList]

    def on_collide(self) -> None:
        if not (
            sprites := arcade.check_for_collision_with_list(
                self, self.targets
            )
        ):
            return

        sprite: arcade.Sprite = sprites[0]
        if not isinstance(sprite, Enemy):
            return

        if self.health == sprite.health:
            self.kill()
            sprite.on_die()
        elif self.health > sprite.health:
            self.health -= sprite.health
            sprite.on_die()
        else:
            sprite.health -= self.health
            self.kill()

    def update(self) -> None:
        super().update()
        self.on_collide()

        if self.is_end() or not self.is_alive():
            self.kill()


@final
class Truck(Reinforcement):
    FILENAME = "./assets/Entities/Vehicles/TankSmall.png"
    HEALTH = 50
    SPEED = 10
