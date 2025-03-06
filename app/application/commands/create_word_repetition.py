from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import (
    LanguageEnum,
    PartOfSpeachEnum,
    RepetitionContentTypeEnum,
    Repetition,
    SlugRepetition,
    WordRepetition,
)
from app.infrastucture.db.session import get_session
from app.infrastucture.repositories.sqlalchemy import SQLAlchemyRepetitionRepository

from ..http.exception import HTTPExceptionResponse


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
    try:
        async with get_session() as session:
            dao = SQLAlchemyRepetitionRepository(session=session)
            repetition: Repetition = await dao.create_repetition(
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

    except Exception as ex:
        return HTTPExceptionResponse(exception=ex)
