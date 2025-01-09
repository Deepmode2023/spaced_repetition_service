from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

class RepetitionContentTypeEnum(str, Enum):
    FILE = RepetitionContentTypeEnum
    WORD = RepetitionContentTypeEnum
    TEXT = RepetitionContentTypeEnum

    @classmethod
    def fields(cls): ...

@dataclass(kw_only=True)
class RepetitionAggragetion:
    slug: str
    title: str
    description: Optional[str]
    document_link: Optional[str]
    user_id: str
    count_repetition: int
    date_repetition: int
    date_last_repetition: Optional[int]
    content_id: str
    content_type: RepetitionContentTypeEnum

    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def to_json(self) -> Dict[str, Optional[int | str]]: ...
