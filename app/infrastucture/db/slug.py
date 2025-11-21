from .base import Base
from uuid import uuid4
from app.domain.models.base import ClassArgument

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .association import repetition_slug_association


class SlugRepetitionSQL(Base):
    __tablename__ = "slug_repetitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, unique=True)
    repetitions = relationship(
        "RepetitionSQL",
        secondary=repetition_slug_association,
        primaryjoin="SlugRepetitionSQL.id == repetition_slug_association.c.slug_id",
        secondaryjoin="RepetitionSQL.id == repetition_slug_association.c.repetition_id",
        back_populates="slugs",
    )
