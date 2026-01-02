from dataclasses import dataclass
from app.domain.common import ClassArgument

@dataclass(kw_only=True)
class SlugRepetition:
    id: int
    name: str
    @classmethod
    def cls_arguments(cls) -> list[ClassArgument]: ...
    @property
    def to_json(self) -> dict[str, str]: ...
