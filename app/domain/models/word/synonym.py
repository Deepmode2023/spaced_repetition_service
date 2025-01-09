from uuid import uuid4

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.infrastucture.db.base import Base


class Synonym(Base):
    """
    Represents a synonym for a word repetition.

    Attributes:
        __tablename__ (str): The name of the database table for this model, "synonyms".
        id (str): A unique identifier for the synonym. Generated using `uuid4()`.
        word_id (str): The foreign key that links this synonym to a `WordRepetition` instance.
        synonym_word (str): The synonym word associated with the `WordRepetition`.

        word (relationship): A relationship to the `WordRepetition` object that this synonym belongs to.
                             This relationship is bi-directional and is managed by `WordRepetition.synonyms`.

    Methods:
        __repr__():
            Provides a string representation of the `Synonym` object.

            Returns:
                str: A string in the format "Synonym(id=<id>, synonym_word=<synonym_word>)".

        to_json():
            Converts the `Synonym` object to a JSON-compatible dictionary.

            Returns:
                dict: A dictionary representation of the `Synonym` object with the following keys:
                      - `id`: The unique identifier of the synonym.
                      - `word_id`: The unique identifier of the associated `WordRepetition`.
                      - `synonym_word`: The synonym word.
    """

    __tablename__ = "synonyms"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    word_id = Column(String(36), ForeignKey("word_repetitions.id"), nullable=False)
    synonym_word = Column(String, nullable=False)

    word = relationship("WordRepetition", back_populates="synonyms")

    def __repr__(self):
        return f"Synonym(id={self.id}, synonym_word={self.synonym_word})"

    @property
    def to_json(self):
        return {
            "id": self.id,
            "word_id": self.word_id,
            "synonym_word": self.synonym_word,
        }
