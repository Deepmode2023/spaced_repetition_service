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

    def __init__(
        self,
        title: str,
        user_id: int,
        id: Optional[int],
        slugs: Optional[list[SlugRepetition]] = None,
        hint: Optional[str] = None,
        count_repetition: Optional[int] = None,
        date_last_repetition: Optional[int] = None,
        content_type: RepetitionContentTypeEnum = RepetitionContentTypeEnum.BASE,
        date_repetition: Optional[int] = None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    @classmethod
    def cls_arguments(cls) -> list[ClassArgument]: ...
    @property
    def to_json(self) -> dict[str, Optional[int | str]]: ...
    def update_repetition_schedule(
        self,
        repetition_status: RepetitionStatusEnum,
    ) -> None: ...
