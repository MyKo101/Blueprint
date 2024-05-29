"""This module contains the Table class."""

# from dataclasses import dataclass
from typing import ClassVar
from typing import Union

# from ..fields.generators import Generator
from ..generators import GeneratorAny
from .metaclass import TableMeta


return_field = Union[list[str], list[int], list[float], list[bool]]


class Table(metaclass=TableMeta):
    """Base Table class."""

    fields: ClassVar[dict[str, GeneratorAny]]

    def __init__(self) -> None:
        """Raise an error if the class is instantiated."""
        raise NotImplementedError("Table class cannot be instantiated.")

    @classmethod
    def generate(cls, n: int) -> dict[str, return_field]:
        """Generate n random records."""
        return {field: cls.fields[field].generate_cache(n) for field in cls.fields}
