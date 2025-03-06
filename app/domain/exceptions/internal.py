from dataclasses import dataclass
from .base import BaseExceptionInternal


@dataclass
class ValidationError(BaseExceptionInternal):
    field_name: str
    field_value: str

    def get_message(self) -> str:
        return f"Validation error on field '{self.field_name}' with value '{self.field_value}'!"


@dataclass
class DatabaseError(BaseExceptionInternal):
    operation: str

    def get_message(self) -> str:
        return f"Database error occurred during '{self.operation}' operation!"


@dataclass
class WrongEnumInstError(BaseExceptionInternal):
    def get_message(self):
        return f"You put the wrong enum type. Please put the correct type enum which will be the instance class EnumABC!"


@dataclass
class WrongEntityError(BaseExceptionInternal):
    entity: str
    entity_type: str
    place: str

    def get_message(self):
        return f"You put the wrong entity {self.entity} in place {self.place}. Please put the correct type {self.entity_type}!"
