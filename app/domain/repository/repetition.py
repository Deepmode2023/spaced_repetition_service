from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..vo import RepetitionContentTypeEnum, PartOfSpeachEnum, LanguageEnum
from ..entities import Repetition, WordRepetition
from app.domain.common.vo import DateType


@dataclass(eq=False, frozen=True)
class IRepetitionRepository(ABC):
    @abstractmethod
    async def get_all_repetitions(
        start_date: DateType,
        end_date: DateType,
        limit: int,
        offset: int,
    ) -> List[Repetition]: ...

    @abstractmethod
    async def update_repetition(
        repetition_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        document_link: Optional[str] = None,
        slugs: Optional[list[str]] = [],
    ) -> bool: ...

    @abstractmethod
    async def create_repetition(
        title: str,
        user_id: str,
        content_type: RepetitionContentTypeEnum,
        description: Optional[str] = None,
        document_link: Optional[str] = None,
        slugs: Optional[list[str]] = [],
        word: Optional[str] = None,
        translate: Optional[list[str]] = None,
        synonyms: Optional[list[str]] = None,
        part_of_speech: Optional[PartOfSpeachEnum] = None,
        examples: Optional[list[str]] = None,
        language: Optional[LanguageEnum] = None,
        context: Optional[str] = None,
        possible_options: Optional[list[str]] = None,
    ) -> WordRepetition: ...

    @abstractmethod
    async def successful_repetition(repetition_id: str) -> bool: ...

    @abstractmethod
    async def unsuccessful_repetition(repetition_id: str) -> bool: ...
