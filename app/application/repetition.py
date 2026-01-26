from dataclasses import dataclass
from functools import partial


from typing import Optional

from app.domain.common.exceptions import DontPassTheMandatoryKey
from app.domain.vo import (
    LanguageEnum,
    PartOfSpeachEnum,
    RepetitionContentTypeEnum,
)
from app.domain.entities import Repetition, WordRepetition, SlugRepetition
from app.domain.common.utils import seive_fields


@dataclass
class RepetitionServices:

    async def create_repetition(
        self,
        type_repetition: RepetitionContentTypeEnum,
        user_id: str,
        title: str,
        slugs: list[str],
        word: Optional[str] = None,
        synonyms: Optional[list[str]] = None,
        part_of_speech: Optional[PartOfSpeachEnum] = None,
        examples: Optional[list[str]] = None,
        possible_options: Optional[list[str]] = None,
        context: Optional[str] = None,
        language: Optional[LanguageEnum] = None,
        translate: Optional[list[str]] = None,
    ) -> Repetition:

        if kwargs.get("slugs", None) is None:
            raise DontPassTheMandatoryKey(key="slugs")

        partial_args = partial(
            seive_fields,
            slugs=slugs,
            user_id=user_id,
            word=word,
            synonyms=synonyms,
            title=title,
        )
        slugs = [SlugRepetition(name=name) for name in kwargs.pop("slugs")]

        match type_repetition:
            case RepetitionContentTypeEnum.WORD:
                _, kwargs = partial_args(
                    required_fields=WordRepetition.cls_arguments() + ["slugs"]
                )
                word: WordRepetition = await self.__word_handler(**kwargs)

            case RepetitionContentTypeEnum.FILE:
                pass

            case RepetitionContentTypeEnum.TEXT:
                pass

            case _:
                from app.domain.common.exceptions import UnknownFieldInsideEnum

                raise UnknownFieldInsideEnum(
                    message="Unknown Repetition content type in Enum",
                    enum=RepetitionContentTypeEnum,
                )

    async def __word_handler(self, **kwargs) -> WordRepetition:

        if kwargs.get("synonyms", None) is None:
            raise DontPassTheMandatoryKey(key="synonyms")

        synonyms = [WordRepetition(word=word) for word in kwargs.pop("synonyms")]

        return WordRepetition(**kwargs, synonyms=synonyms)
