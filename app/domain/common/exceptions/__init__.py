from .base import BaseExceptionInternal, BaseExceptionExternal
from .external import UnknownFieldInsideEnum, DontPassTheMandatoryKey
from .internal import (
    DatabaseError,
    ValidationError,
    WrongEntityError,
    WrongEnumInstError,
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
]
