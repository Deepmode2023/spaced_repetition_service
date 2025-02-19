from enum import Enum

from sqlalchemy import ARRAY, Column, String
from sqlalchemy.orm import relationship

from app.infrastucture.db.base import Base

from .association import synonym_association


class PartOfSpeachEnum(str, Enum):
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


class LanguageEnum(str, Enum):
    ENGLISH_US = "en-US"
    ENGLISH_BR = "en_GB"
    SPANISH = "es"
    FRENCH = "fr"
    GERMANY = "de"

    @classmethod
    def fields(cls):
        """
        Returns all fields of the enum as a dictionary.

        Returns:
            dict: A dictionary with enum names as keys and values as enum values.
        """
        return {item.name: item.value for item in cls}


class WordRepetition(Base):
    """
    Attributes:
        __tablename__ (str): The name of the database table for this model, "word_repetitions".

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
    synonyms = relationship(
        "WordRepetition",
        secondary=synonym_association,
        primaryjoin="WordRepetition.id == synonym_association.c.word_id",
        secondaryjoin="WordRepetition.id == synonym_association.c.synonym_id",
        backref="related_words",
    )
    part_of_speech = Column(String(20), nullable=True)
    examples = Column(ARRAY(String), nullable=True)
    language = Column(String(30), default=LanguageEnum.ENGLISH_BR)
    context = Column(String, nullable=True)
    possible_options = Column(ARRAY(String), nullable=True)
    image_url = Column(String, nullable=True)

    def __repr__(self):
        return f"WordRepetition(id={self.id}, word={self.word})"

    @property
    def to_json(self):

        return {
            "word": self.word,
            "translate": self.translate,
            "synonyms": [synonym.to_json for synonym in self.synonyms],
            "part_of_speech": self.part_of_speech,
            "examples": self.examples,
            "language": self.language,
            "context": self.context,
            "possible_options": self.possible_options,
            "image_url": self.image_url,
        }

    @classmethod
    def cls_arguments(cls) -> list[str]:
        return [
            "word",
            "translate",
            "synonyms",
            "part_of_speach",
            "examples",
            "language",
            "context",
            "possible_options",
            "image_url",
        ]
