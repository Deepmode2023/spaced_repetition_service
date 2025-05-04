from enum import Enum
from ..enum import EnumABC

class PartOfSpeachEnum(EnumABC):
    NOUN: str
    PRONOUN: str
    VERB: str
    ADJECTIVE: str
    ADVERB: str
    PREPOSITION: str
    CONJUNCTION: str
    INTERJECTION: str

    @classmethod
    def fields(cls) -> dict[str, str]: ...
    @classmethod
    def get_name(self): ...

class LanguageEnum(EnumABC):
    ENGLISH_US: str
    ENGLISH_BR: str
    SPANISH: str
    FRENCH: str
    GERMANY: str
    POLAND: str

    @classmethod
    def fields(cls) -> dict[str, str]: ...
    @classmethod
    def get_name(self): ...

class WordRepetition:
    def __init__(
        self,
        id: str,
        word: str,
        translate: str,
        synonyms: list[str],
        part_of_speech: PartOfSpeachEnum,
        examples: list[str],
        language: LanguageEnum,
        context: str,
        possible_options: list[str],
        image_url: str,
    ): ...
    @property
    def to_json(self) -> dict[str, any]: ...
    @classmethod
    def cls_arguments(cls) -> list[str]: ...

class WordRepetitionSchema:
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
