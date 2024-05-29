"""Metaclass for table classes."""

from __future__ import annotations

from typing import Any
from typing import Callable

from ..generators import Generator
from ..generators import to_generator


def is_function(value: Any) -> bool:
    """Check if the value is callable.

    Args:
        value (Any): The value to check.

    Returns:
        bool: True if the value is callable, False otherwise.
    """
    return (
        callable(value)
        or isinstance(value, staticmethod)
        or isinstance(value, classmethod)
    )


def is_field(key: str, value: Any) -> bool:
    """Check if the value is a field.

    Args:
        key (str): The key of the value.
        value (Any): The value to check.

    Returns:
        bool: True if the value is a field, False otherwise.
    """
    return not (key.startswith("_") or is_function(value))


def demote_conditional(
    dct: dict[str, Any], key: str, predicate: Callable[[str, Any], bool]
) -> dict[str, Any]:
    """Demote items in a dictionary based on a predicate.

    Args:
        dct (dict[str, Any]): The dictionary to demote items from.
        key (str): The key to move the demoted items to.
        predicate (Callable[[str, Any], bool]):
            The predicate to determine if an item should be demoted.

    Returns:
        dict[str, Any]: The dictionary with the demoted items removed.
    """
    demoted: dict[str, Any] = {}
    for k, v in dct.items():
        if not predicate(k, v):
            continue
        demoted[k] = v

    for k in demoted.keys():
        del dct[k]

    if key in dct.keys():
        demoted.update(dct[key])

    dct[key] = demoted

    return demoted


class TableMeta(type):
    """Metaclass for table classes."""

    def __new__(
        cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]  # noqa:B902
    ) -> TableMeta:
        """Create a new table class."""
        print(f"Creating new table class {name!r}:")
        fields = demote_conditional(dct, "fields", is_field)
        for k, v in fields.items():
            print(f"   {k}: {v}")
            if not isinstance(v, Generator):
                dct["fields"][k] = to_generator(v)

        return super().__new__(cls, name, bases, dct)
