"""The resolve function."""

from typing import TypeVar
from typing import Union

from ..generators import Generator


T = TypeVar("T", int, float, bool, str)


def resolve(obj: Union[T, Generator[T]], n: int) -> Union[T, list[T]]:
    """Return the resolved value of the object.

    Args:
        obj (T | Generator[T]): The object to resolve.
        n (int): The number of values to generate.

    Returns:
        T | list[T]: The resolved value of the object.
    """
    if isinstance(obj, Generator):
        return obj.generate(n)
    return obj
