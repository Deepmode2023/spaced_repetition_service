from dataclasses import dataclass

from typing import Dict, Optional
from .word.word_repetition import WordRepetitionSchema
from app.infrastucture.db.base import ClassArgument
from pydantic import BaseModel
from app.domain.models.enum import EnumABC
from app.domain.models.slug.slug import SlugRepetitionSchema, SlugRepetition

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

class RepetitionSchema(BaseModel):
    id: str
    slugs: list[SlugRepetitionSchema]
    title: str
    description: Optional[str]
    document_link: Optional[str]
    user_id: str
    count_repetition: int
    date_repetition: int
    date_last_repetition: Optional[int]
    content_type: RepetitionContentTypeEnum
