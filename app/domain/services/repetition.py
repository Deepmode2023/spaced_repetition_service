from dataclasses import dataclass, field
from functools import partial
from typing import Optional, Callable

from app.domain.models.repetition import Repetition
from app.domain.models.slug.slug import SlugRepetition

from ..exceptions import DontPassTheMandatoryKey, UnknownFieldInsideEnum
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
        user_id: str,
        title: str,
        slugs: list[str],
        dependency_repetition: WordRepetition,
    ) -> Repetition:
        """
        Creates a Repetition object without any session-related operations.

        Args:
            content_type (RepetitionContentTypeEnum): The type of repetition (WORD, MD, TEXT).
            user_id (str): The ID of the user associated with the repetition.
            title (str): The title for the repetition.
            slugs (List[str]): A list of slug names to be converted into SlugRepetition objects.
            dependency_repetition (WordRepetition): The WordRepetition object that acts as a dependency.

        Returns:
            Repetition: A new Repetition object populated with the provided information.
        """

        return Repetition(
            slugs=self._create_slugs(slugs),
            user_id=user_id,
            title=title,
            content_type=content_type,
            content_id=dependency_repetition.id,
        )

    def create_dependency_repetition_model(
        self,
        content_type: RepetitionContentTypeEnum,
        **kwargs,
    ) -> None:
        """
        Creates a dependency repetition object based on the repetition type.

        This method creates a dependency repetition, such as WordRepetition,
        based on the provided repetition type (e.g., WORD, MD, TEXT).

        Args:
            content_type (RepetitionContentTypeEnum): The type of repetition to create.
            **kwargs: Additional arguments that will be used to create the repetition.

        Raises:
            UnknownFieldInsideEnum: If the provided repetition type is not recognized.
        """
        partial_kwargs = partial(handle_arguments, **kwargs)

        if content_type == RepetitionContentTypeEnum.WORD:
            _, kwargs = partial_kwargs(white_list_keys=WordRepetition.cls_arguments())
            return self._create_word_dependency_repetition_model(**kwargs)
        elif content_type == RepetitionContentTypeEnum.MD:
            pass
        elif content_type == RepetitionContentTypeEnum.TEXT:
            pass
        else:
            raise UnknownFieldInsideEnum(
                message="Unknown Repetition content type in Enum",
                enum=RepetitionContentTypeEnum,
            )

    def _create_word_dependency_repetition_model(self, **kwargs) -> WordRepetition:
        """
        Creates a WordRepetition object, ensuring mandatory fields are provided.

        Args:
            **kwargs: Arguments for creating a WordRepetition object.

        Returns:
            WordRepetition: A new WordRepetition object created with the provided arguments.

        Raises:
            DontPassTheMandatoryKey: If the required 'synonyms' field is not provided.
        """

        if "synonyms" not in kwargs:
            raise DontPassTheMandatoryKey(key="synonyms")

        synonyms = [WordRepetition(word=word) for word in kwargs.pop("synonyms")]

        word = WordRepetition(**kwargs, synonyms=synonyms)
        print(f"-====> {word.to_json}")
        return word

    def _create_slugs(self, slugs: list[str]) -> list[SlugRepetition]:
        """
        Creates SlugRepetition objects from the provided list of slug names.

        Args:
            slugs (List[str]): A list of slug names to be converted to SlugRepetition objects.

        Returns:
            List[SlugRepetition]: A list of SlugRepetition objects created from the provided slugs.

        Raises:
            DontPassTheMandatoryKey: If the 'slugs' argument is empty or None.
        """
        if not slugs:
            raise DontPassTheMandatoryKey(key="slugs")

        return [SlugRepetition(name=name) for name in slugs]
