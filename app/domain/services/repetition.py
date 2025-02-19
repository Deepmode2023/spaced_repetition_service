from dataclasses import dataclass, field
from functools import partial
from typing import Optional

from app.domain.models.repetition import Repetition
from app.domain.models.slug.slug import SlugRepetition

from ..exceptions import DontPassTheMandatoryKey
from ..models import (
    LanguageEnum,
    PartOfSpeachEnum,
    RepetitionContentTypeEnum,
    WordRepetition,
)
from ..utils import handle_arguments


@dataclass
class RepetitionServices:
    async def create_repetition(
        self,
        type_repetition: RepetitionContentTypeEnum,
        user_id: str,
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

        partial_args = partial(
            handle_arguments,
            slugs=slugs,
            user_id=user_id,
            word=word,
            synonyms=synonyms,
            part_of_speech=part_of_speech,
            examples=examples,
            possible_options=possible_options,
            context=context,
            language=language,
            translate=translate,
        )

        match type_repetition:
            case RepetitionContentTypeEnum.WORD:
                _, kwargs = partial_args(
                    white_list_keys=WordRepetition.cls_arguments() + ["slugs"]
                )
                word: WordRepetition = await self.__word_handler(**kwargs)

            case RepetitionContentTypeEnum.FILE:
                pass

            case RepetitionContentTypeEnum.TEXT:
                pass

            case _:
                from app.domain.exceptions import UnknownFieldInsideEnum

                raise UnknownFieldInsideEnum(
                    message="Unknown Repetition content type in Enum",
                    enum=RepetitionContentTypeEnum,
                )

    async def __word_handler(self, **kwargs) -> WordRepetition:
        if kwargs.get("slugs", None) is None:
            raise DontPassTheMandatoryKey(key="slugs")
        if kwargs.get("synonyms", None) is None:
            raise DontPassTheMandatoryKey(key="synonyms")

        self.__make_slugs(slugs=kwargs.pop("slugs"))
        synonyms = [WordRepetition(word=word) for word in kwargs.pop("synonyms")]

        return WordRepetition(**kwargs, synonyms=synonyms)
    

    
    def __make_slugs(self, slugs: list[str]):
        self.slugs = [SlugRepetition(name=slug_name) for slug_name in slugs]