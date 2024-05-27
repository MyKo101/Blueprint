"""Random Value Generators."""

from __future__ import annotations

import random


def random_int(low: int, high: int) -> int:
    """Generate a random integer between low and high.

    Args:
        low (int): The lower bound of the random integer.
        high (int): The upper bound of the random integer.

    Returns:
        int: A random integer between low and high.
    """
    return random.randint(low, high)  # noqa: S311


def random_float(low: float, high: float) -> float:
    """Generate a random float between low and high.

    Args:
        low (float): The lower bound of the random float.
        high (float): The upper bound of the random float.

    Returns:
        float: A random float between low and high.
    """
    return random.uniform(low, high)  # noqa: S311


def random_bool(probability: float) -> bool:
    """Generate a random boolean with probability p.

    Args:
        probability (float):
            The probability of the random boolean being True.

    Returns:
        bool: A random boolean with probability p.
    """
    return random.random() < probability  # noqa: S311
