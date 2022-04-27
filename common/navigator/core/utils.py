"""Generic utility functions."""

import time


def get_timestamp() -> str:
    """Return a string representing the current date and time."""
    return time.strftime("%Y%m%d-%H%M")
