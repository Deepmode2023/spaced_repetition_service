from enum import Enum
from uuid import uuid4

import pendulum
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.infrastucture.db.base import Base


class SlugRepetition(str, Enum):
    FILE = "FILE"
    TEXT = "TEXT"


class Repetition(Base):
    __tablename__ = "repetitions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    slug = Column(String(20), nullable=True, default=SlugRepetition.FILE)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    document_link = Column(String, nullable=True)
    user_id = Column(String, nullable=False)
    count_repetition = Column(Integer, default=0)
    date_repetition = Column(Integer, nullable=False, default=pendulum.now().date)
    date_last_repetition = Column(Integer, nullable=True)

    def __repr__(self):
        return f"SpacedRepetiotionsModel(id={self.id}, title={self.title})"

    def __eq__(self, other):
        if isinstance(other, Repetition):
            return (
                self.slug == other.slug
                and self.title == other.title
                and self.user_id == other.user_id
            )
        return False

    @property
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "user_id": self.user_id,
            "count_repetition": self.count_repetition,
            "date_repetition": self.date_repetition,
            "date_last_repetition": self.date_last_repetition,
        }
