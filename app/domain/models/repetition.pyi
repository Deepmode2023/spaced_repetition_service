from dataclasses import dataclass

from typing import Dict, Optional
from app.domain.models.base import ClassArgument
from app.domain.models.enum import EnumABC
from app.domain.models.slug import SlugRepetition

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
    id: str
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
    def to_json(self) -> Dict[str, Optional[int | str]]: ...
