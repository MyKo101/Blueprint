"""RandomInt field generator."""

from __future__ import annotations

import random
from dataclasses import dataclass

from .generators import GeneratorBool
from .generators import GeneratorFloat
from .generators import GeneratorInt


def generate_int(low: int, high: int) -> int:
    """Generate a random integer between low and high.

    Args:
        low (int): The lower bound of the random integer.
        high (int): The upper bound of the random integer.

    Returns:
        int: A random integer between low and high.
    """
    return random.randint(low, high)  # noqa: S311


def generate_float(low: float, high: float) -> float:
    """Generate a random float between low and high.

    Args:
        low (float): The lower bound of the random float.
        high (float): The upper bound of the random float.

    Returns:
        float: A random float between low and high.
    """
    return random.uniform(low, high)  # noqa: S311


def generate_bool(probability: float) -> bool:
    """Generate a random boolean with probability p.

    Args:
        probability (float): The probability of the random boolean being True.

    Returns:
        bool: A random boolean with probability p.
    """
    return random.random() < probability  # noqa: S311


@dataclass
class RandomInt(GeneratorInt):
    """A Generator that generates random integers."""

    low: int
    high: int

    def generate(self, n: int) -> list[int]:
        """Generate n random integers between low and high."""
        return [generate_int(self.low, self.high) for _ in range(n)]

    def copy(self) -> RandomInt:
        """Return a copy of the RandomInt object."""
        return RandomInt(self.low, self.high)


@dataclass
class RandomFloat(GeneratorFloat):
    """A Generator that generates random floats."""

    low: int
    high: int

    def generate(self, n: int) -> list[float]:
        """Generate n random integers between low and high."""
        return [generate_float(self.low, self.high) for _ in range(n)]

    def copy(self) -> RandomFloat:
        """Return a copy of the RandomFloat object."""
        return RandomFloat(self.low, self.high)


@dataclass
class RandomBool(GeneratorBool):
    """A Generator that generates random booleans."""

    probability: float

    def generate(self, n: int) -> list[bool]:
        """Generate n random integers between low and high."""
        return [generate_bool(self.probability) for _ in range(n)]

    def copy(self) -> RandomBool:
        """Return a copy of the RandomBool object."""
        return RandomBool(self.probability)
