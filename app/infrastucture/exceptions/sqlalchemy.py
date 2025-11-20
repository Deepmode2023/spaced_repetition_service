from app.domain.exceptions.base import BaseExceptionExternal
from dataclasses import dataclass, field


@dataclass
class DuplicateAddedEntity(BaseExceptionExternal):
    status = 409
    fields: list[str] = field(default_factory=list)

    def get_message(self):
        return f"Entity with this fields = {", ".join(self.fields)} already exists"
