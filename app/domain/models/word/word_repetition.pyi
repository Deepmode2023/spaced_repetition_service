from enum import Enum

class PartOfSpeachEnum(str, Enum):
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

class LanguageEnum(str, Enum):
    ENGLISH_US: str
    ENGLISH_BR: str
    SPANISH: str
    FRENCH: str
    GERMANY: str

    @classmethod
    def fields(cls) -> dict[str, str]: ...

class WordRepetition:
    def __init__(
        self,
        id: str,
        word: str,
        translate: str,
        synonyms: list[WordRepetition],
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
