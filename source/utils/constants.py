# /utils/constants.py
"""`Constants` module containing utility constants."""


# Define Base Game Constants
# Define Map & Screen Constants
TILE_SIZE = 64
SCREEN_TITLE = "Tower Defender"
SCREEN_WIDTH = 15 * TILE_SIZE
SCREEN_HEIGHT = 10 * TILE_SIZE
SCREEN_HALF_W = SCREEN_WIDTH // 2
SCREEN_HALF_H = SCREEN_HEIGHT // 2

# Define Game Scene Constants
LAYER_REINFORCEMENTS = "Reinforcements"
LAYER_WAYPOINTS = "Waypoints"
LAYER_LOCATIONS = "Locations"
LAYER_PARTICLES = "Particles"
LAYER_ENEMIES = "Enemies"
LAYER_TOWERS = "Towers"
LAYER_SLOTS = "Slots"
LAYER_COINS = "Coins"
LAYER_UI = "UI"


# Define Typographic Constants
# Define Font Constants
FONT = "Kenney Future Narrow"
FONT_TITLE = 50
FONT_LARGE = 24
FONT_MEDIUM = 12
FONT_SMALL = 8

# Define Anchor Position Constant
ANCHOR_CENTER = "center"
ANCHOR_TOP = "top"
ANCHOR_BOTTOM = "bottom"
ANCHOR_LEFT = "left"
ANCHOR_RIGHT = "right"


# Define UI Constants
# Define UI Colours
BLACK = (21, 19, 21)
GREY = (80, 80, 80)
WHITE = (255, 255, 255)
TRANSPARENT_DARK = (*BLACK, 150)
TRANSPARENT_LIGHT = (*BLACK, 50)
HEALTHBAR_COLOUR = (79, 189, 101)

# Define Stat UI Constants
STAT_UI_WIDTH = 92
STAT_UI_HEIGHT = 3
STAT_UI_OFFSET = 35
STAT_UI_MARGIN = 2
STAT_UI_OUTLINE = 2
STAT_UI_FULL_W = STAT_UI_WIDTH + STAT_UI_MARGIN
STAT_UI_HALF_W = STAT_UI_WIDTH // 2
STAT_UI_FULL_H = STAT_UI_HEIGHT + STAT_UI_MARGIN
STAT_UI_LARGE_HEIGHT = STAT_UI_FULL_H * 3
STAT_UI_LARGE_OFFSET = STAT_UI_OFFSET + STAT_UI_LARGE_HEIGHT

# Define Info UI Constants
INFO_UI_WIDTH = 3 * SCREEN_WIDTH // 5
INFO_UI_HEIGHT = 20
INFO_UI_MARGIN = 4
INFO_UI_SMALL_WIDTH = INFO_UI_WIDTH // 3
INFO_UI_FULL_W = INFO_UI_WIDTH + INFO_UI_MARGIN
INFO_UI_FULL_H = INFO_UI_HEIGHT + INFO_UI_MARGIN
INFO_UI_HALF_H = INFO_UI_FULL_H // 2


# Define Game Constants
# Define Initial Gameplay Constants
GAMEPLAY_HEALTH = 100
MINIMUM_HEALTH = 0
MINIMUM_COIN = 0

# Define Game Data Constants
DATA_PATH = "./data.json"
DEFAULT_DATA = {
    "Easy": True,
    "Medium": False,
    "Hard": False,
}

# Define Game Tips Constants
TIPS_COOLDOWN = 2500
TIPS_DATA = (
    "Select an empty slot to place defenses!",
    "Right click on a tower to sell!",
    "Reinforcements have cooldown timers!",
    "Do you know: The tank boss drops gold? Not very useful though.",
    "Do you know: Rocket can one shot almost everything?",
    "Do you know: The silver coin used to be bronze?",
    "Do you know: Rocket does splash damage? Like a real rocket!",
    "Do you know: Reinforcement tank is more powerful than rocket?",
)
