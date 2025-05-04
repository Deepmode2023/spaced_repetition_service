from dataclasses import dataclass
from functools import partial

from app.domain.models.repetition import Repetition
from app.domain.models.slug.slug import SlugRepetition

from ..exceptions.external import DontPassTheMandatoryKey, UnknownFieldInsideEnum
from ..models import (
    LanguageEnum,
    PartOfSpeachEnum,
    RepetitionContentTypeEnum,
    WordRepetition,
)
from ..utils import handle_arguments


@dataclass
class RepetitionServices:
    def create_repetition_model(
        self,
        content_type: RepetitionContentTypeEnum,
        **kwargs,
    ) -> WordRepetition:
        partial_kwargs = partial(handle_arguments, content_type=content_type, **kwargs)

        if content_type == RepetitionContentTypeEnum.WORD:
            _, kwargs = partial_kwargs(white_list_keys=WordRepetition.cls_arguments())

            return self._create_word_repetition_model(**kwargs)
        elif content_type == RepetitionContentTypeEnum.MD:
            pass
        elif content_type == RepetitionContentTypeEnum.TEXT:
            pass
        else:
            raise UnknownFieldInsideEnum(
                message="Unknown Repetition content type in Enum",
                enum=RepetitionContentTypeEnum,
            )

    def _create_word_repetition_model(self, slugs, title, **kwargs) -> WordRepetition:
        if "synonyms" not in kwargs:
            raise DontPassTheMandatoryKey(key="synonyms")
        synonyms = kwargs.pop("synonyms")

        return WordRepetition(
            **kwargs,
            synonyms=synonyms,
            title=title,
            slugs=self._create_slugs(slugs),
        )

    def _create_slugs(self, slugs: list[str]) -> list[SlugRepetition]:
        if not slugs:
            raise DontPassTheMandatoryKey(key="slugs")

        return [SlugRepetition(name=name) for name in slugs]
