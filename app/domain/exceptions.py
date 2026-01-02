from dataclasses import dataclass, field
from app.domain.common.exceptions import BaseExceptionExternal


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
