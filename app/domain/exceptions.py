from dataclasses import dataclass
from typing import Optional

from .base import BaseException


@dataclass(frozen=True)
class RepetitionAlreadyExistsError(BaseException):
    repetition_title: str
    status = 409

    def get_message(self) -> str:
        return f"Repetition '{self.repetition_title}' already exists. {self.message}"


@dataclass(frozen=True)
class RepetitionNotFoundError(BaseException):
    repetition_id: int
    status = 404

    def get_message(self) -> str:
        return (
            f"Repetition with ID '{self.repetition_id}' was not found. {self.message}"
        )


@dataclass(frozen=True)
class ValidationError(BaseException):
    field_name: str
    field_value: str
    status = 409

    def get_message(self) -> str:
        return f"Validation error on field '{self.field_name}' with value '{self.field_value}'. {self.message}"


@dataclass(frozen=True)
class DatabaseError(BaseException):
    operation: str
    status = 409

    def get_message(self) -> str:
        return f"Database error occurred during '{self.operation}' operation. {self.message}"
