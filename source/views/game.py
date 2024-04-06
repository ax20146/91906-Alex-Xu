# /views/game.py
"""`Game` module containing the `Game` class."""


# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from ..entities.buttons import Button
from ..entities.entities.enemies import Enemy
from ..entities.entities.entities import Entity
from ..entities.entities.reinforcements import Reinforcement, reinforcements
from ..entities.entities.tanks import Canon
from ..entities.particles.coins import Coin
from ..entities.particles.particles import Particle
from ..entities.slots import Slot
from ..entities.turrets.towers import Tower, towers
from ..utils import Clock, Sprite, Timer, Vector, View
from ..utils.constants import (
    ANCHOR_CENTER,
    FONT,
    FONT_MEDIUM,
    GAMEPLAY_HEALTH,
    HEALTHBAR_COLOUR,
    INFO_UI_FULL_H,
    INFO_UI_FULL_W,
    INFO_UI_HALF_H,
    INFO_UI_HEIGHT,
    INFO_UI_MARGIN,
    INFO_UI_SMALL_WIDTH,
    INFO_UI_WIDTH,
    LAYER_COINS,
    LAYER_ENEMIES,
    LAYER_LOCATIONS,
    LAYER_PARTICLES,
    LAYER_REINFORCEMENTS,
    LAYER_SLOTS,
    LAYER_TOWERS,
    LAYER_UI,
    LAYER_WAYPOINTS,
    MINIMUM_COIN,
    MINIMUM_HEALTH,
    SCREEN_HALF_W,
    SCREEN_HEIGHT,
    TILE_SIZE,
    TRANSPARENT_DARK,
    WHITE,
)
from ..utils.types import Any, Iterator, NamedTuple, Type
from ..wave import Wave, wave
from . import endscreens


# Define Map data structure
class Map(NamedTuple):
    name: str
    tilemap: arcade.TileMap


# Define Game class
class Game(View):
    """`Game` object represents the main game view.

    Inherited from `View`.

    Implements the functionality of main game view.
    """

    def __init__(self, tilemap: str) -> None:
        """Initialise a `Game` view object.

        Args:
            tilemap (str): The name of the tilemap to load.
        """

        # Initialised parent class
        super().__init__()

        # Define tuple of map name & tilemap object
        self.map: Map = Map(
            tilemap,
            arcade.load_tilemap(f"./maps/{tilemap}.tmx"),
        )

        # Define view's scene, clock, timer attributes
        self.scene: arcade.Scene = arcade.Scene.from_tilemap(self.map.tilemap)
        self.clock: Clock = Clock()
        self.timer: Timer = Timer(self.clock)

        # Define mouse interaction attributes
        self.select: Sprite | None = None
        self.hover: Sprite | None = None

        # Define gameplay attributes
        self.wave = wave()
        self.health: int = GAMEPLAY_HEALTH
        self.display: str = ""
        self.coin: int = MINIMUM_COIN

        # Process & setup the game
        self.process_locations()
        self.setup_scene()
        self.setup_classes()
        self.setup_ui()

    # Setup functions
    @staticmethod
    def process_waypoints(tilemap: arcade.TileMap) -> Iterator[Vector]:
        """Process the map waypoints data into a iterator of vectors.

        Args:
            tilemap (arcade.TileMap): The tilemap to process.

        Returns:
            Iterator[Vector]: The iterator containing all waypoints.
        """
        WAYPOINT = 0

        return (
            Vector(*waypoint)
            for waypoint in (
                tilemap.object_lists[LAYER_WAYPOINTS][WAYPOINT].shape
            )
            if isinstance(waypoint, tuple)
        )

    def process_locations(self) -> None:
        """Process the map locations data into slot sprites objects."""

        for slot in self.scene[LAYER_LOCATIONS]:
            self.scene.add_sprite(LAYER_SLOTS, Slot(Vector(*slot.position)))

    def setup_scene(self) -> None:
        """Setup the game scene with all the required sprite lists."""

        # Remove unused sprite lists
        self.scene.remove_sprite_list_by_name(LAYER_LOCATIONS)

        # Add required sprite lists
        self.scene.add_sprite_list(LAYER_COINS)
        self.scene.add_sprite_list(LAYER_TOWERS)
        self.scene.add_sprite_list(LAYER_ENEMIES)
        self.scene.add_sprite_list(LAYER_REINFORCEMENTS)
        self.scene.add_sprite_list(LAYER_PARTICLES)

    def setup_classes(self) -> None:
        """Setup all the sprite class variable to access game state."""

        # Assign required data to all sprites
        Sprite.clock = self.clock

        # Assign required data to all enemy entities
        Enemy.waypoints = tuple(self.process_waypoints(self.map.tilemap))
        Enemy.sprite_list = self.scene[LAYER_ENEMIES]
        Enemy.targets = self.scene[LAYER_REINFORCEMENTS]

        # Assign required data to all reinforcement entities
        Reinforcement.waypoints = tuple(reversed(Enemy.waypoints))
        Reinforcement.sprite_list = self.scene[LAYER_REINFORCEMENTS]
        Reinforcement.targets = self.scene[LAYER_ENEMIES]

        # Assign required data to all tower entities
        Tower.sprite_list = self.scene[LAYER_TOWERS]
        Tower.targets = self.scene[LAYER_ENEMIES]

        # Assign required data particles & coins
        Coin.sprite_list = self.scene[LAYER_COINS]
        Particle.sprite_list = self.scene[LAYER_PARTICLES]

    def setup_ui(self) -> None:
        """Setup the button UI sprites of the game."""

        # Setup all the tower buttons at particular location
        for idx, (obj, path) in enumerate(towers.items(), start=1):
            position = Vector(TILE_SIZE, TILE_SIZE * (9 * idx - 1) // 8)
            self.scene.add_sprite(LAYER_UI, Button(path, position, obj))

        # Setup all the reinforcement button  at particular location
        for idx, (obj, path) in enumerate(reinforcements.items(), start=2):
            position = Vector(TILE_SIZE * (9 * idx - 1) // 8, TILE_SIZE)
            self.scene.add_sprite(LAYER_UI, Button(path, position, obj))

    # Draw functions
    def on_draw(self) -> None:
        """The draw function called every cycle (tick)."""

        # Draw all the sprites
        self.clear()
        self.scene.draw()

        # Draw the mouse hovered sprites
        if isinstance(self.hover, (Entity, Slot, Button)) and (
            self.hover in self.scene[LAYER_SLOTS]
            or self.hover in self.scene[LAYER_ENEMIES]
            or self.hover in self.scene[LAYER_REINFORCEMENTS]
            or self.hover in self.scene[LAYER_UI]
        ):
            self.hover.on_hover_draw()
        else:
            self.hover = None

        # Draw the mouse selected sprites
        if isinstance(self.select, (Entity, Slot)) and (
            self.select in self.scene[LAYER_SLOTS]
            or self.select in self.scene[LAYER_ENEMIES]
            or self.select in self.scene[LAYER_REINFORCEMENTS]
        ):
            self.select.on_select_draw()
        else:
            self.select = None

        # Draw the extra information from the button sprites
        for sprite in (
            sprite
            for sprite in self.scene[LAYER_UI]
            if isinstance(sprite, Button)
        ):
            sprite.on_draw()

        # Draw the game UI elements
        self.draw_healthbar()
        self.draw_infobar(f"${self.coin:,}", INFO_UI_WIDTH)
        self.draw_infobar(self.display, INFO_UI_SMALL_WIDTH)

    def draw_healthbar(self) -> None:
        """Draw the player's healthbar UI."""

        arcade.draw_rectangle_filled(
            SCREEN_HALF_W,
            SCREEN_HEIGHT - INFO_UI_HALF_H,
            width=INFO_UI_FULL_W,
            height=INFO_UI_FULL_H,
            color=TRANSPARENT_DARK,
        )
        arcade.draw_rectangle_filled(
            SCREEN_HALF_W,
            SCREEN_HEIGHT - INFO_UI_HALF_H,
            width=(max(self.health, MINIMUM_HEALTH) / GAMEPLAY_HEALTH)
            * INFO_UI_WIDTH,
            height=INFO_UI_HEIGHT,
            color=HEALTHBAR_COLOUR,
        )
        arcade.draw_text(
            f"{max(self.health, MINIMUM_HEALTH)} / {GAMEPLAY_HEALTH}",
            SCREEN_HALF_W,
            SCREEN_HEIGHT - INFO_UI_HALF_H,
            font_name=FONT,
            font_size=FONT_MEDIUM,
            anchor_x=ANCHOR_CENTER,
            anchor_y=ANCHOR_CENTER,
            color=WHITE,
        )

    def draw_infobar(self, text: str, start_x: int) -> None:
        """Draw trapezium shaped information UI.

        Args:
            text (str): The text information to display.
            start_x (int): The starting position of the information UI.
        """

        # Calculate all the points of the trapezium shape
        RATIO = 2
        end_x = start_x + INFO_UI_SMALL_WIDTH
        start_y = SCREEN_HEIGHT - INFO_UI_FULL_H - INFO_UI_MARGIN
        end_y = start_y - INFO_UI_FULL_H

        # Draw the trapezium shape
        arcade.draw_polygon_filled(
            color=TRANSPARENT_DARK,
            point_list=(
                (start_x, start_y),
                (end_x, start_y),
                (end_x - INFO_UI_MARGIN * INFO_UI_MARGIN, end_y),
                (start_x + INFO_UI_MARGIN * INFO_UI_MARGIN, end_y),
            ),
        )

        # Draw the text information displayed on the UI bar
        arcade.draw_text(
            text,
            start_x=(start_x + end_x) // RATIO,
            start_y=start_y - INFO_UI_HALF_H,
            font_name=FONT,
            font_size=FONT_MEDIUM,
            anchor_x=ANCHOR_CENTER,
            anchor_y=ANCHOR_CENTER,
            color=WHITE,
        )

    # Update functions
    def on_update(self, delta_time: float) -> None:
        """The update function called every cycle (tick).

        Args:
            delta_time (float): The change in time since last tick.
        """

        # Update the game clock & sprites
        self.clock.update(delta_time)
        self.scene.update()

        # Update the various aspect of the game
        self.update_health()
        self.update_state()
        self.update_wave()

        # Update the button class with current game state
        Button.update_data(self.coin, self.select)

    def update_state(self) -> None:
        """Update the current game state (Win/Lose)."""

        # Determine whether the player lost & change view when lost
        if self.health <= MINIMUM_HEALTH:
            self.on_draw()
            self.window.show_view(endscreens.Defeat())
            return

        # Determine whether the player won & change views when won
        if self.timer.disable and not len(self.scene[LAYER_ENEMIES]):
            self.on_draw()
            self.window.show_view(endscreens.Victory(self.map.name))
            return

    def update_health(self) -> None:
        """Update the health information of the player."""

        # Iterate all enemies & determine if player should take damage
        for sprite in (
            sprite
            for sprite in self.scene[LAYER_ENEMIES]
            if isinstance(sprite, Enemy) and sprite.is_end()
        ):
            self.health -= sprite.on_end()

    def update_wave(self) -> None:
        """Update the game based on the `wave` generator function."""

        # Determine if enough time has passed since last game event
        if not self.timer.available():
            return

        # Determine if the wave generator is exhausted
        try:
            wave_data = next(self.wave)

        # Disable the timer on the final wave (wave generator exhausted)
        except StopIteration:
            self.timer.disable = True
            return

        # Update the timer's duration based on wave generator
        if isinstance(wave_data, int):
            self.timer.duration = wave_data
            return

        # Update the display text & player coin based on wave generator
        if isinstance(wave_data, Wave):
            self.display = wave_data.display
            self.coin += wave_data.coin
        else:
            wave_data()

        # Update the timer for next iteration
        self.timer.duration = 0
        self.timer.update()

    # Mouse press event functions
    def on_mouse_press(self, x: int, y: int, button: int, *args: Any) -> None:
        """The mouse press event function called.

        Args:
            x (int): The x position of mouse press.
            y (int): The y position of mouse press.
            button (int): The mouse button that pressed.
        """

        # Call the left mouse function when left mouse press
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.on_mouse_left(x, y)

        # Call the right mouse function when right mouse press
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.on_mouse_right(x, y)

    def on_mouse_left(self, x: int, y: int) -> None:
        """The mouse left press event function called.

        Args:
            x (int): The x position of mouse press.
            y (int): The y position of mouse press.
        """

        # Call button `on_click()` event function when button pressed
        if sprite := self.mouse_over(
            (x, y), self.scene[LAYER_UI], type=Button
        ):
            self.coin -= sprite.on_click()
            return

        # Determine the currently selected game sprite
        self.on_select((x, y))

    def on_mouse_right(self, x: int, y: int) -> None:
        """The mouse right press event function called.

        Args:
            x (int): The x position of mouse press.
            y (int): The y position of mouse press.
        """

        # Call slot `on_sell()` event function when pressed
        if sprite := self.mouse_over(
            (x, y), self.scene[LAYER_SLOTS], type=Slot
        ):
            self.coin += sprite.on_sell()

    def on_select(self, xy: tuple[int, int]) -> None:
        """The mouse selection event function called.

        Args:
            xy (tuple[int, int]): The xy position of mouse press.
        """

        # Assign the game mouse selection from the following lists
        self.select = (
            self.mouse_over(xy, self.scene[LAYER_SLOTS])
            or self.mouse_over(xy, self.scene[LAYER_REINFORCEMENTS])
            or self.mouse_over(xy, self.scene[LAYER_ENEMIES])
        )

    # Mouse move event functions
    def on_mouse_motion(self, x: int, y: int, *args: Any) -> None:
        """The mouse motion event function called.

        Args:
            x (int): The x position of mouse press.
            y (int): The y position of mouse press.
        """

        # Determine the currently hovered game sprite
        self.on_hover((x, y))

        # Update all coins with cursor position
        Coin.target = Vector(x, y)

        # Call coin `on_collect` event function when mouse overed
        if sprite := self.mouse_over(
            (x, y), self.scene[LAYER_COINS], type=Coin
        ):
            self.coin += sprite.on_collect()

    def on_hover(self, xy: tuple[int, int]) -> None:
        """The mouse hover event function called.

        Args:
            xy (tuple[int, int]): The xy position of mouse press.
        """

        # Assign the game mouse hover from the following lists
        self.hover = (
            self.mouse_over(xy, self.scene[LAYER_UI])
            or self.mouse_over(xy, self.scene[LAYER_SLOTS])
            or self.mouse_over(xy, self.scene[LAYER_ENEMIES])
            or self.mouse_over(xy, self.scene[LAYER_REINFORCEMENTS])
        )

    # Mouse interaction functions
    @staticmethod
    def mouse_over(
        xy: tuple[int, int],
        lst: arcade.SpriteList,
        *,
        type: type[Type] = Sprite,
    ) -> Type | None:
        """Determine the top most sprite at the given position.

        Args:
            xy (tuple[int, int]): The position to search at.
            lst (arcade.SpriteList): The list of sprites to search from.
            type (type[Type], optional):
            The type of sprite that should be searched.
                Defaults to Sprite.

        Returns:
            Type | None: The top most sprite of
            given type at given position from given list.
            (None if it can't be found).
        """
        TOP = -1
        SECOND_TOP = -2

        # Filter all the sprite in the given list with correct type
        sprites: list[Type] = [
            sprite
            for sprite in arcade.get_sprites_at_point(xy, lst)
            if isinstance(sprite, type)
        ]

        # Determine if sprites is empty (No sprites found)
        if not sprites:
            return

        # Return the top most sprite, or second top most if the top
        # is tank canon to select the tank body instead
        if isinstance(sprites[TOP], Canon) and len(sprites) >= -SECOND_TOP:
            return sprites[SECOND_TOP]
        return sprites[TOP]
