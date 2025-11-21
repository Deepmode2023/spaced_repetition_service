from dataclasses import dataclass
from typing import Dict
from app.domain.models.base import ClassArgument

@dataclass(kw_only=True)
class SlugRepetition:
    id: str
    name: str
    @classmethod
    def cls_arguments(cls) -> list[ClassArgument]: ...
    @property
    def to_json(self) -> Dict[str, str]: ...
