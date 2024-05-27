"""RandomInt field generator."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TypeVar

from .generators import Generator
from .generators import GeneratorBool
from .generators import GeneratorFloat
from .generators import GeneratorInt
from .reference_types import ReferenceFloat
from .reference_types import ReferenceInt
from .zipper import Zipper


T = TypeVar("T", int, float, bool, str)


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


def actualise(obj: T | Generator[T], n: int) -> T | list[T]:
    """Return the actual value of the object."""
    if isinstance(obj, Generator):
        return obj.generate(n)
    return obj


@dataclass
class RandomInt(GeneratorInt):
    """A Generator that generates random integers."""

    low: ReferenceInt
    high: ReferenceInt

    def generate(self, n: int) -> list[int]:
        """Generate n random integers between low and high."""
        low_z = actualise(self.low, n)
        high_z = actualise(self.high, n)
        return [
            generate_int(low, high) for low, high in Zipper(low_z, high_z, length=n)
        ]

    def copy(self) -> RandomInt:
        """Return a copy of the RandomInt object."""
        return RandomInt(self.low, self.high)


@dataclass
class RandomFloat(GeneratorFloat):
    """A Generator that generates random floats."""

    low: ReferenceFloat
    high: ReferenceFloat

    def generate(self, n: int) -> list[float]:
        """Generate n random integers between low and high."""
        low_z = actualise(self.low, n)
        high_z = actualise(self.high, n)
        return [
            generate_float(low, high) for low, high in Zipper(low_z, high_z, length=n)
        ]

    def copy(self) -> RandomFloat:
        """Return a copy of the RandomFloat object."""
        return RandomFloat(self.low, self.high)


@dataclass
class RandomBool(GeneratorBool):
    """A Generator that generates random booleans."""

    probability: ReferenceFloat

    def generate(self, n: int) -> list[bool]:
        """Generate n random integers between low and high."""
        probability = actualise(self.probability, n)
        return [generate_bool(prob) for (prob,) in Zipper(probability, length=n)]

    def copy(self) -> RandomBool:
        """Return a copy of the RandomBool object."""
        return RandomBool(self.probability)
