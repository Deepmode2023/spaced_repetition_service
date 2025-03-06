from dataclasses import dataclass, field
from .base import BaseExceptionExternal
from ..models.enum import EnumABC


@dataclass
class RepetitionAlreadyExistsError(BaseExceptionExternal):
    repetition_title: str
    status: int = field(default=409)

    def get_message(self) -> str:
        return f"Repetition '{self.repetition_title}' already exists."


@dataclass
class RepetitionNotFoundError(BaseExceptionExternal):
    repetition_id: int
    status: int = field(default=409)

    def get_message(self) -> str:
        return f"Repetition with ID '{self.repetition_id}' was not found."


@dataclass
class UnknownFieldInsideEnum(BaseExceptionExternal):
    enum: EnumABC
    status: int = field(default=409)

    def get_message(self) -> str:
        return f"Unknown field inside enum {self.enum.__class__.name}. Possible options {self.enum.fields()}."


@dataclass
class DontPassTheMandatoryKey(BaseExceptionExternal):
    key: str
    status: int = field(default=409)

    def get_message(self):
        return f"You do not pass the mandatory key [{self.key}]. It is mandatory for the system."


@dataclass
class RepetitionAlreadyExistsError(BaseExceptionExternal):
    repetition_title: str
    status: int = field(default=409)

    def get_message(self) -> str:
        return f"Repetition '{self.repetition_title}' already exists."


@dataclass
class RepetitionNotFoundError(BaseExceptionExternal):
    repetition_id: int
    status: int = field(default=409)

    def get_message(self) -> str:
        return f"Repetition with ID '{self.repetition_id}' was not found."
