from dataclasses import dataclass
from typing import Dict

@dataclass(kw_only=True)
class SlugRepetition:
    id: str
    name: str

    @property
    def to_json(self) -> Dict[str, str]: ...
