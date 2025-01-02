from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

class SlugRepetition(str, Enum):
    FILE = str
    TEXT = str

@dataclass(kw_only=True)
class Repetition:
    slug: str
    title: str
    description: Optional[str]
    document_link: Optional[str]
    user_id: str
    count_repetition: int
    date_repetition: int
    date_last_repetition: Optional[int]

    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def to_json(self) -> Dict[str, Optional[int | str]]: ...
