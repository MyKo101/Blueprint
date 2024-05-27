"""Reference types for the generators."""

from typing import Union

from .generators import GeneratorBool
from .generators import GeneratorFloat
from .generators import GeneratorInt
from .generators import GeneratorStr


ReferenceInt = Union[int, GeneratorInt]
ReferenceFloat = Union[float, GeneratorFloat]
ReferenceStr = Union[str, GeneratorStr]
ReferenceBool = Union[bool, GeneratorBool]
ReferenceNumeric = Union[int, GeneratorInt, float, GeneratorFloat]
