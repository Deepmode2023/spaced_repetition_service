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
        return f"Repetition '{self.repetition_title}' already exists. { f"Addiction info: {self.message}" if self.message else ""}"


@dataclass(frozen=True)
class RepetitionNotFoundError(BaseException):
    repetition_id: int
    status: 404

    def get_message(self) -> str:
        return f"Repetition with ID '{self.repetition_id}' was not found. { f"Addiction info: {self.message}" if self.message else ""}"


@dataclass(frozen=True)
class ValidationError(BaseException):
    field_name: str
    field_value: str
    status: 409

    def get_message(self) -> str:
        return f"Validation error on field '{self.field_name}' with value '{self.field_value}'. { f"Addiction info: {self.message}" if self.message else ""}"


@dataclass(frozen=True)
class DatabaseError(BaseException):
    operation: str
    status: 409

    def get_message(self) -> str:
        return f"Database error occurred during '{self.operation}' operation. { f"Addiction info: {self.message}" if self.message else ""}"


@dataclass(frozen=True, kw_only=True)
class UnknownFieldInsideEnum(BaseException):
    status: int = 409
    enum: EnumABC

    def get_message(self) -> str:
        return f"Unknown field inside enum {self.enum.__class__.name}. Possible options {self.enum.fields()}. { f"Addiction info: {self.message}" if self.message else ""}"


@dataclass(frozen=True, kw_only=True)
class DontPassTheMandatoryKey(BaseException):
    status: int = 409
    key: str

    def get_message(self):
        return f"You do not pass the mandatory key [{self.key}]. It is mandatory for the system. { f"Addiction info: {self.message}" if self.message else ""}"
