from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum, EnumMeta

from .base import BaseException


class ABCEnumMeta(ABCMeta, EnumMeta):
    pass


class EnumABC(Enum, metaclass=ABCEnumMeta):
    @abstractmethod
    def fields(self):
        pass


@dataclass(frozen=True)
class RepetitionAlreadyExistsError(BaseException):
    repetition_title: str
    status: 409

    def get_message(self) -> str:
        return f"Repetition '{self.repetition_title}' already exists. {self.message}"


@dataclass(frozen=True)
class RepetitionNotFoundError(BaseException):
    repetition_id: int
    status: 404

    def get_message(self) -> str:
        return (
            f"Repetition with ID '{self.repetition_id}' was not found. {self.message}"
        )


@dataclass(frozen=True)
class ValidationError(BaseException):
    field_name: str
    field_value: str
    status: 409

    def get_message(self) -> str:
        return f"Validation error on field '{self.field_name}' with value '{self.field_value}'. {self.message}"


@dataclass(frozen=True)
class DatabaseError(BaseException):
    operation: str
    status: 409

    def get_message(self) -> str:
        return f"Database error occurred during '{self.operation}' operation. {self.message}"


@dataclass(frozen=True, kw_only=True)
class UnknownFieldInsideEnum(BaseException):
    status: int = 409
    enum: EnumABC

    def get_message(self) -> str:
        return f"Unknown field inside enum {self.enum.__class__.name}. Possible options {self.enum.fields()}. Addiction message: {self.message}"
