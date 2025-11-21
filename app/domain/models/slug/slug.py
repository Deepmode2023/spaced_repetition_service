from uuid import UUID
from dataclasses import dataclass

from app.domain.models.base import ClassArgument


@dataclass
class SlugRepetition:
    id: UUID
    name: str

    def __repr__(self):
        return f"SlugRepetition(id={self.id}, name={self.name})"

    @classmethod
    def cls_arguments(cls):
        return [ClassArgument(field="name", nullable=False)]

    @property
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }
