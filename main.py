# /main.py
"""The main program entry point."""


# Import Local Dependencies
from source import *


# Define main function
def main() -> None:
    """The main program function."""

    window: Window = create_window()
    window.run()


# Run main function
if __name__ == "__main__":
    main()
