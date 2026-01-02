from dataclasses import dataclass, field

from app.domain.common import ClassArgument, seq


@dataclass
class SlugRepetition:
    name: str
    id: int = field(default_factory=lambda: next(seq))

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
