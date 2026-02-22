from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..vo import PartOfSpeachEnum, LanguageEnum
from ..entities import Repetition, WordRepetition, MDRepetition
from app.domain.common.vo import DateType, URL


@dataclass(eq=False, frozen=True)
class IRepetitionRepository(ABC):
    @abstractmethod
    async def get_all_repetitions(
        self,
        start_date: DateType,
        end_date: DateType,
        limit: int,
        offset: int,
        tags: Optional[str] = [],
    ) -> List[Repetition]: ...

    @abstractmethod
    async def get_study_repetitions(
        self,
        limit: int,
        offset: int,
        tags: Optional[str] = [],
    ) -> List[Repetition]: ...

    @abstractmethod
    async def update_repetition(
        self,
        id: str,
        title: Optional[str] = None,
        document_link: Optional[str] = None,
        slugs: Optional[list[str]] = [],
        hint: Optional[str] = None,
        count_repetition: Optional[int] = None,
        date_repetition: Optional[int] = None,
        date_last_repetition: Optional[int] = None,
    ) -> bool: ...

    @abstractmethod
    async def create_repetition(
        self,
        title: str,
        user_id: str,
        slugs: Optional[list[str]] = [],
        hint: Optional[str] = None,
    ) -> Repetition: ...

    @abstractmethod
    async def create_word_repetition(
        self,
        title: str,
        user_id: str,
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
    async def create_md_repetition(
        self,
        title: str,
        user_id: str,
        document: bytes,
        document_link: Optional[URL] = None,
        slugs: Optional[list[str]] = [],
    ) -> MDRepetition: ...

    @abstractmethod
    async def successful_repetition(self, repetition_id: str) -> bool: ...

    @abstractmethod
    async def unsuccessful_repetition(self, repetition_id: str) -> bool: ...
