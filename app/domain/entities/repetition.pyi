from dataclasses import dataclass
from app.domain.common.models import ClassArgument, EnumABC
from typing import Optional

from .slug import SlugRepetition

class RepetitionStatusEnum(EnumABC):
    SUCCESSFUL = RepetitionStatusEnum
    UNSUCCESSFUL = RepetitionStatusEnum
    STARTING = RepetitionStatusEnum

    @classmethod
    def fields(cls): ...
    @classmethod
    def get_name(self): ...

class RepetitionContentTypeEnum(EnumABC):
    MD = RepetitionContentTypeEnum
    WORD = RepetitionContentTypeEnum
    TEXT = RepetitionContentTypeEnum

    @classmethod
    def fields(cls): ...
    @classmethod
    def get_name(self): ...

@dataclass(kw_only=True)
class Repetition:
    id: int
    slugs: list[SlugRepetition]
    hint: str
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
    @classmethod
    def cls_arguments(cls) -> list[ClassArgument]: ...
    @property
    def to_json(self) -> dict[str, Optional[int | str]]: ...

def calc_date_repetition(
    count_repetition: int,
    repetition_status: Optional[RepetitionStatusEnum],
    date_repetition: Optional[int],
) -> int: ...
