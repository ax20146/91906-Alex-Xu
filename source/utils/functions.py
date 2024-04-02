# /utils/functions.py
"""`Functions` module containing utility functions."""


# Import Built-in Dependencies
from json import dump, load
from random import choice

# Import Local Dependencies
from .constants import DATA_PATH, TIPS_DATA


# Define Generate Tips function
def generate_tips() -> str:
    """Randomly generate and returns and tip for the game.

    Returns:
        str: The randomly generated tip.
    """

    return choice(TIPS_DATA)


# Define Data Read function
def read_data() -> dict[str, bool]:
    """Read the game progression data from disk.

    Returns:
        dict[str, bool]: The game progression data.
    """

    # Read data from disk
    with open(DATA_PATH) as file:
        return load(file)


# Define Data Write function
def write_data(data: dict[str, bool]) -> None:
    """Write the game progression data to disk.

    Args:
        data (dict[str, bool]): The game progression data.
    """

    # Write data to disk
    with open(DATA_PATH, "w") as file:
        dump(data, file)


# Define Data Process function
def process_data(string: str, data: dict[str, bool]) -> dict[str, bool]:
    """Process the game progression data.

    Args:
        string (str): The current game progression.
        data (dict[str, bool]): The game progression data.

    Returns:
        dict[str, bool]: A processed game progression data.
    """

    # Make a copy of the data dictionary
    data = data.copy()

    # Find the key in data dictionary to update
    lst: list[str] = list(data)
    idx: int = lst.index(string) + 1

    # Update the data (if able)
    if idx < len(lst):
        data[lst[idx]] = True

    # Return the modified copy of data dictionary
    return data
