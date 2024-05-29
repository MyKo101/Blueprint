"""Module for converting constant values to Generators."""

from typing import TypeVar
from typing import Union
from typing import overload

from .generators import GeneratorConstantBool
from .generators import GeneratorConstantFloat
from .generators import GeneratorConstantInt
from .generators import GeneratorConstantStr


T = TypeVar("T", int, bool, str, float)

return_types = Union[
    GeneratorConstantBool,
    GeneratorConstantInt,
    GeneratorConstantFloat,
    GeneratorConstantStr,
]


@overload
def to_generator(x: bool) -> GeneratorConstantBool:  # type:ignore
    # type ignore is here because bool is considered a subclass of int
    ...


@overload
def to_generator(x: int) -> GeneratorConstantInt:  # <
    ...


@overload
def to_generator(x: float) -> GeneratorConstantFloat:  # <
    ...


@overload
def to_generator(x: str) -> GeneratorConstantStr:  # <
    ...


def to_generator(x: T) -> return_types:
    """Convert a constant value to a Generator.

    Args:
        x (T): The constant value to convert.

    Raises:
        ValueError: If the value cannot be converted to a Generator.

    Returns:
        return_types: The converted Generator.
    """
    # if isinstance(x, Generator):
    #     return x
    if isinstance(x, bool):
        return GeneratorConstantBool(x)
    if isinstance(x, int):
        return GeneratorConstantInt(x)
    if isinstance(x, float):
        return GeneratorConstantFloat(x)
    if isinstance(x, str):
        return GeneratorConstantStr(x)
    raise ValueError(f"Cannot convert {x} to a Generator.")
