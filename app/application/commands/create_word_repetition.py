from uuid import UUID
from app.domain.models import (
    LanguageEnum,
    PartOfSpeachEnum,
    RepetitionContentTypeEnum,
    Repetition,
    SlugRepetition,
    WordRepetition,
)
from dataclasses import dataclass


@dataclass
class CreateWordQuery:
    user_id: UUID
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
    user_id: UUID
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


async def create_word_repetition(
    user_id: str,
    word: str,
    synonyms: list[str],
    part_of_speech: PartOfSpeachEnum,
    examples: list[str],
    possible_options: list[str],
    context: str,
    language: LanguageEnum,
    translate: list[str],
    slugs: list[str],
    title: str,
):
    async with get_session() as session:
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
