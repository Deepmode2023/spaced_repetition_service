from enum import Enum

from core.db import Base
from core.utils import compare_uuid
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship


class SlugRepetition(str, Enum):
    FILE = "FILE"
    TEXT = "TEXT"


class SpacedRepetition(Base):
    __tablename__ = "spaced_repetition"

    id = Column(Integer, primary_key=True)
    slug = Column(String(20), nullable=False, default=SlugRepetition.FILE)
    title = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    document_link = Column(String, nullable=True)
    user_id = Column(String, nullable=False)
    count_repetition = Column(Integer, default=0)
    date_repetition = Column(DateTime(timezone=True), nullable=False)
    date_last_repetition = Column(DateTime(timezone=True), nullable=False)

    def __repr__(cls):
        return f"SpacedRepetiotionsModel(id={cls.id}, title={cls.title})"

    def __eq__(cls, other):
        if isinstance(other, SpacedRepetition):
            return (
                cls.slug == other.slug
                and cls.title == other.title
                and compare_uuid(cls.user_id, other.user_id)
            )
        return False

    @property
    def toJson(
        cls,
    ):
        return {
            "id": cls.id,
            "title": cls.title,
            "slug": cls.slug,
            "description": cls.description,
            "user_id": cls.user_id,
            "count_repetition": cls.count_repetition,
            "date_repetition": cls.date_repetition,
            "date_last_repetition": cls.date_last_repetition,
        }
