from app.domain.entities import Repetition, SlugRepetition, WordRepetition
from app.domain.vo import LanguageEnum, PartOfSpeachEnum, RepetitionContentTypeEnum
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastucture.repositories.sqlalchemy import SQLAlchemyRepetitionRepository


@dataclass
class CreateWordQuery:
    user_id: int
    word: str
    synonyns: list[str]
    part_of_speech: PartOfSpeachEnum
    examples: list[str]
    possible_options: list[str]
    context: str
    language: LanguageEnum
    translate: list[str]
    slugs: list[str]
    title: str


@dataclass
class CreateWordHadnler:
    user_id: int
    word: str
    synonyns: list[str]
    part_of_speech: PartOfSpeachEnum
    examples: list[str]
    possible_options: list[str]
    context: str
    language: LanguageEnum
    translate: list[str]
    slugs: list[str]
    title: str
    session: AsyncSession


async def create_word_repetition(
    user_id: str,
    word: str,
    synonyms: list[str],
    part_of_speech: PartOfSpeachEnum,
    examples: list[str],
    possible_options: list[str],
    context: str,
    title: str,
    session: AsyncSession,
    language: LanguageEnum,
    translate: list[str],
    slugs: list[str],
):
    rep = SQLAlchemyRepetitionRepository(session=session)
    repetition: WordRepetition = await rep.create_repetition(
        title=title,
        content_type=RepetitionContentTypeEnum.WORD,
        user_id=user_id,
        word=word,
        synonyms=synonyms,
        part_of_speech=part_of_speech,
        examples=examples,
        possible_options=possible_options,
        context=context,
        language=language,
        translate=translate,
        slugs=slugs,
    )
    return repetition
