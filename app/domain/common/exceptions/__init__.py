from .base import BaseExceptionInternal, BaseExceptionExternal
from .external import UnknownFieldInsideEnum, DontPassTheMandatoryKey, WrongIDType
from .internal import (
    DatabaseError,
    ValidationError,
    WrongEntityError,
    WrongEnumInstError,
    IncorrectURLString,
)

__all__ = [
    "BaseExceptionInternal",
    "BaseExceptionExternal",
    "UnknownFieldInsideEnum",
    "DatabaseError",
    "ValidationError",
    "WrongEntityError",
    "WrongEnumInstError",
    "DontPassTheMandatoryKey",
    "WrongIDType",
    "IncorrectURLString",
]
