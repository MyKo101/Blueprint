"""Metaclass for table classes."""

from __future__ import annotations

from typing import Any
from typing import Callable


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
) -> None:
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

    if key not in dct.keys():
        dct[key] = {}
    dct[key].update(demoted)

    return None


class TableMeta(type):
    """Metaclass for table classes."""

    @staticmethod
    def demote_fields(dct: dict[str, Any]) -> dict[str, Any]:
        """Extract fields from the class dictionary."""
        fields: dict[str, Any] = {}
        for k, v in dct.items():
            if not is_field(k, v):
                continue
            fields[k] = v

        for k in fields.keys():
            del dct[k]

        if "fields" not in dct.keys():
            dct["fields"] = {}
        dct["fields"].update(fields)

        return dct

    def __new__(
        cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]  # noqa:B902
    ) -> TableMeta:
        """Create a new table class."""
        # print(f"Creating class {name}")
        # print(f"{cls=}")
        # print(f"{bases=}")
        # print("dct:")
        # for k, v in dct.items():
        # print(f"  {k} = {v}")
        demote_conditional(dct, "fields", is_field)
        # print("dct after:")
        # for k, v in dct.items():
        # print(f"  {k} = {v}")

        return super().__new__(cls, name, bases, dct)
