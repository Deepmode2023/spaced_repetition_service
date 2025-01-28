from dataclasses import dataclass
from functools import partial
from typing import Optional

from app.domain.models.repetition import RepetitionAggragetion
from app.domain.models.word.synonym import Synonym

from ..models import (
    LanguageEnum,
    PartOfSpeachEnum,
    RepetitionContentTypeEnum,
    Synonym,
    WordRepetition,
)
from ..utils import handle_arguments


@dataclass
class RepetitionServices:
    async def create_repetition(
        self,
        type_repetition: RepetitionContentTypeEnum,
        user_id: str,
        word: Optional[str] = None,
        synonyms: Optional[list[str]] = None,
        part_of_speech: Optional[PartOfSpeachEnum] = None,
        examples: Optional[list[str]] = None,
        possible_options: Optional[list[str]] = None,
        context: Optional[str] = None,
        language: Optional[LanguageEnum] = None,
        translate: Optional[list[str]] = None,
    ) -> RepetitionAggragetion:
        partial_args = partial(
            handle_arguments,
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
                _, kwargs = partial_args(white_list_keys=WordRepetition.cls_arguments())
                await self.__word_handler(**kwargs)

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

    async def __word_handler(self, **kwargs):
        try:

            synonyms = [
                Synonym(synonym_word=synonym) for synonym in kwargs.get("synonyms", [])
            ]

            repetition = WordRepetition(**kwargs)

            if len(synonyms) > 0:
                repetition.synonyms.extend(synonyms)

            print(f"KSKDSKDKSk")
        except Exception as ex:
            print(f"sdfsdfsdf {ex}")
