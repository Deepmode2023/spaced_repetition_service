from .base import BaseExceptionExternal
from ..models import EnumABC
from dataclasses import dataclass, field


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
