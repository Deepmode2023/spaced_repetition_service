from enum import Enum
from uuid import uuid4

from sqlalchemy import Column, String

from app.infrastucture.db.base import Base

from .word.word_repetition import WordRepetition


class RepetitionContentTypeEnum(str, Enum):
    FILE = "file"
    WORD = "word"
    TEXT = "text"

    @classmethod
    def fields(cls):
        """
        Returns all fields of the enum as a dictionary.

        Returns:
            dict: A dictionary with enum names as keys and values as enum values.
        """
        return {item.name: item.value for item in cls}


class RepetitionAggragetion(Base):
    __tablename__ = "repetitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    content_type = Column(String, nullable=False)
    content_id = Column(String(36), nullable=False)

    @property
    def content(self):
        from ..exceptions import UnknownFieldInsideEnum

        if self.content_type == RepetitionContentTypeEnum.WORD:
            return self.session.query(WordRepetition).get(self.content_id)
        elif self.content_type == RepetitionContentTypeEnum.FILE:
            return
            # return self.session.query(FileRepetition).get(self.content_id)
        elif self.content_type == RepetitionContentTypeEnum.TEXT:
            # return self.session.query(TextRepetition).get(self.content_id)
            return
        else:
            raise UnknownFieldInsideEnum(
                message=f"Unknown content_type: {self.content_type}",
                enum=RepetitionContentTypeEnum,
            )

    @property
    def to_json(self):
        data = {
            "id": self.id,
            "content_type": self.content_type,
            "content_id": self.content_id,
        }
        if hasattr(self.content, "to_json"):
            data.update(self.content.to_json)

        return data
