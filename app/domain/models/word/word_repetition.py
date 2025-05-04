from sqlalchemy import ARRAY, Column, String, Enum as SQLEnum, ForeignKeyConstraint

from pydantic import BaseModel
from ..enum import EnumABC
from app.domain.models.repetition import Repetition, RepetitionSchema
from app.infrastucture.db.base import ClassArgument


class PartOfSpeachEnum(EnumABC):
    NOUN = "NOUN"
    PRONOUN = "PRONOUN"
    VERB = "VERB"
    ADJECTIVE = "ADJECTIVE"
    ADVERB = "ADVERB"
    PREPOSITION = "PREPOSITION"
    CONJUNCTION = "CONJUNCTION"
    INTERJECTION = "INTERJECTION"

    @classmethod
    def fields(cls):
        """
        Returns all fields of the enum as a dictionary.

        Returns:
            dict: A dictionary with enum names as keys and values as enum values.
        """
        return {item.name: item.value for item in cls}

    @classmethod
    def get_name(self):
        return "partofspeachenum"


class LanguageEnum(EnumABC):
    ENGLISH_US = "EN-US"
    ENGLISH_BR = "EN_GB"
    SPANISH = "ES"
    FRENCH = "FR"
    GERMANY = "DE"
    POLAND = "PL"

    @classmethod
    def fields(cls):
        """
        Returns all fields of the enum as a dictionary.

        Returns:
            dict: A dictionary with enum names as keys and values as enum values.
        """
        return {item.name: item.value for item in cls}

    @classmethod
    def get_name(self):
        return "languageenum"


class WordRepetition(Repetition):
    from app.domain.models.repetition import RepetitionContentTypeEnum

    """
    Attributes:
        __tablename__ (str): The name of the database table for this model, "word_repetitions".
        id (str): iditeficator
        word (str): name word
        translate (list of str): A list of translations for the word.
        synonyms (relationship): A relationship to the `Synonym` objects associated with this word.
                                 Managed as a bi-directional relationship via `Synonym.word`.
                                 Changes cascade automatically with "all, delete-orphan".
        part_of_speech (str): The part of speech of the word (e.g., noun, verb, adjective).
        examples (list of str): A list of example sentences or phrases demonstrating the word's usage.
        language (str): The language of the word. Defaults to `LanguageEnum.ENGLISH_BR`.
        context (str, optional): Additional context or notes for the word.
        possible_options (list of str, optional): Possible alternative translations or variations for the word.
        image_url (str, optional): A URL pointing to an image associated with the word.

    Methods:
        to_json():
            Converts the `WordRepetition` object to a JSON-compatible dictionary by combining data from the parent class
            and the additional fields defined in this class.

            Returns:
                dict: A dictionary representation of the `WordRepetition` object with the following keys:
                      - Fields specific to `WordRepetition`:
                        - `translate`: List of translations for the word.
                        - `synonyms`: List of associated synonyms, represented as dictionaries via `Synonym.to_json`.
                        - `part_of_speech`: The part of speech of the word.
                        - `examples`: List of example sentences or phrases.
                        - `language`: The language of the word.
                        - `context`: Additional context for the word.
                        - `possible_options`: Possible alternative translations or variations.
                        - `image_url`: A URL for an associated image.

    """

    __tablename__ = "word_repetitions"
    id = Column(String(36), primary_key=True)
    word = Column(String, unique=True, nullable=False)
    translate = Column(ARRAY(String), nullable=True)
    synonyms = Column(ARRAY(String), nullable=True)
    part_of_speech = Column(
        SQLEnum(
            PartOfSpeachEnum,
            name=PartOfSpeachEnum.get_name(),
            create_type=False,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=True,
    )
    examples = Column(ARRAY(String), nullable=True)
    language = Column(
        SQLEnum(
            LanguageEnum,
            name=LanguageEnum.get_name(),
            create_type=False,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=LanguageEnum.ENGLISH_BR,
    )
    context = Column(String, nullable=True)
    possible_options = Column(ARRAY(String), nullable=True)
    image_url = Column(String, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["id"], ["repetitions.id"], name="fk_word_repetitions_repetition_id"
        ),
    )

    __mapper_args__ = {
        "polymorphic_identity": RepetitionContentTypeEnum.WORD.value,
    }

    def __repr__(self):
        return f"WordRepetition(id={self.id}, word={self.word})"

    @property
    def to_json(self):
        return {
            "id": self.id,
            "word": self.word,
            "translate": self.translate,
            "synonyms": self.synonyms,
            "part_of_speech": self.part_of_speech,
            "examples": self.examples,
            "language": self.language,
            "context": self.context,
            "possible_options": self.possible_options,
            "image_url": self.image_url,
            **super().to_json,
        }

    @classmethod
    def cls_arguments(cls) -> list[ClassArgument]:
        return [
            ClassArgument(field="word", nullable=False),
            ClassArgument(field="translate", nullable=True),
            ClassArgument(field="synonyms", nullable=True),
            ClassArgument(field="part_of_speech", nullable=True),
            ClassArgument(field="examples", nullable=True),
            ClassArgument(field="language", nullable=True),
            ClassArgument(field="context", nullable=True),
            ClassArgument(field="possible_options", nullable=True),
            ClassArgument(field="image_url", nullable=True),
            *super().cls_arguments(),
        ]


class WordRepetitionModel(BaseModel):
    id: str
    word: str
    translate: str
    synonyms: list[str]
    part_of_speech: PartOfSpeachEnum
    examples: list[str]
    language: LanguageEnum
    context: str
    possible_options: list[str]
    image_url: str


class WordRepetitionSchema(RepetitionSchema):
    pass
