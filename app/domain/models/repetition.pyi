from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

class RepetitionStatusEnum(str, Enum):
    SUCCESSFUL = RepetitionStatusEnum
    UNSUCCESSFUL = RepetitionStatusEnum

    @classmethod
    def fields(cls): ...

class RepetitionContentTypeEnum(str, Enum):
    FILE = RepetitionContentTypeEnum
    WORD = RepetitionContentTypeEnum
    TEXT = RepetitionContentTypeEnum

    @classmethod
    def fields(cls): ...

@dataclass(kw_only=True)
class Repetition:
    id: str
    slugs: str
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
