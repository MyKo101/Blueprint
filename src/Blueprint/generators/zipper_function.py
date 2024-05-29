"""zipper function."""

from __future__ import annotations

import sys
from itertools import repeat
from typing import TYPE_CHECKING
from typing import Collection
from typing import Iterable
from typing import TypeVar
from typing import Union

from typing_extensions import TypeGuard


T = TypeVar("T")

if TYPE_CHECKING:
    zt = Union[zip[tuple[T, ...]], zip[tuple[T, ...]]]
    rt = repeat[T]
else:
    zt = zip
    rt = repeat

if sys.version_info >= (3, 10):

    def zip_strict(*args: Iterable[T]) -> zt[T]:
        """Return a zip object.

        Args:
            args (Iterable[T] | T): The arguments to zip.

        Returns:
            zip[tuple[T, ...]]: A zip object.
        """
        return zip(*args, strict=True)

else:

    def zip_strict(*args: Iterable[T]) -> zt[T]:
        """Return a zip object. For compatibility with Python 3.9 and below.

        Args:
            args (Iterable[T] | T): The arguments to zip.

        Returns:
            zip[tuple[T, ...]]: A zip object.
        """
        return zip(*args)  # noqa: B905


def is_collection(obj: Collection[T] | T) -> TypeGuard[Collection[T]]:
    """Return True if the object is (probably) a Collection.

    Args:
        obj (Any): The object to check.

    Returns:
        bool: True if the object is a Collection.
    """
    if (
        hasattr(obj, "__iter__")
        and hasattr(obj, "__len__")
        and not isinstance(obj, str)
    ):
        return callable(obj.__iter__)
    return False


def is_not_collection(obj: Collection[T] | T) -> TypeGuard[T]:
    """Return True if the object is (probably) not a Collection.

    Args:
        obj (Any): The object to check.

    Returns:
        bool: True if the object is not a Collection.
    """
    return not is_collection(obj)


def zipper(*args: Collection[T] | T, length: int | None = None) -> zt[T]:
    """Return a zip object.

    Args:
        args (Collection[T] | T): The arguments to zip.
        length (int | None): The length of the zip object.

    Raises:
        ValueError: If length is less than 1.
        ValueError: If length does not match the length of provided lists.
        ValueError: If the provided lists are not the same length.

    Returns:
        zip[tuple[T, ...]]: A zip object.
    """
    if length is not None and length < 1:
        raise ValueError("Parameter length must be greater than 0.")

    arg_lengths = [len(a) for a in args if is_collection(a)]
    if length is not None and any(a != length for a in arg_lengths):
        raise ValueError("Parameter length must match the length of provided lists.")

    arg_lengths_set = set(arg_lengths)
    if len(arg_lengths_set) > 1:
        raise ValueError("All provided lists must be the same length.")

    arg_length = arg_lengths_set.pop() if len(arg_lengths_set) > 0 else length
    length = 1 if arg_length is None else arg_length

    normalised_args_nones: list[Collection[T] | rt[T] | None] = [
        (
            arg
            if is_collection(arg)
            else repeat(arg, length) if is_not_collection(arg) else None
        )
        for arg in args
    ]

    normalised_args = (arg for arg in normalised_args_nones if arg is not None)

    return zip_strict(*normalised_args)
