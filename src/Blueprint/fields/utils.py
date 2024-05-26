"""This module contains utility functions"""
from __future__ import annotations

import sys
from typing import TypeVar


# This file is needed to support Python 3.9 and below
# If support for 3.9 is dropped, all instances of
# zip_strict can be replaced with the built-in zip function
# using the strict=True argument

T = TypeVar("T")

if sys.version_info < (3, 10):

    def zip_strict(x: list[T], y: list[T]) -> zip[tuple[T, T]]:
        """Zip two lists together.

        Args:
            x (list[T]): The first list.
            y (list[T]): The second list.

        Returns:
            zip[tuple[T, T]]: The zipped lists.

        """
        return zip(x, y)  # noqa: B905

else:

    def zip_strict(x: list[T], y: list[T]) -> zip[tuple[T, T]]:
        """Zip two lists together.

        Args:
            x (list[T]): The first list.
            y (list[T]): The second list.

        Returns:
            zip[tuple[T, T]]: The zipped lists.

        """
        return zip(x, y, strict=True)
