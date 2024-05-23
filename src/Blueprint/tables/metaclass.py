"""Metaclass for table classes."""

from __future__ import annotations

from typing import Any


class TableMeta(type):
    """Metaclass for table classes."""

    def __new__(
        cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]  # noqa:B902
    ) -> TableMeta:
        """Create a new table class."""
        print(f"Creating class {name}")
        return super().__new__(cls, name, bases, dct)
