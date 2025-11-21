from .base import Base
from uuid import uuid4
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.domain.models import RepetitionContentTypeEnum, calc_date_repetition
from .association import repetition_slug_association


class RepetitionSQL(Base):
    __tablename__ = "repetitions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    content_type = Column(
        SQLEnum(
            RepetitionContentTypeEnum,
            name=RepetitionContentTypeEnum.get_name(),
            create_type=False,
        ),
        nullable=False,
        default=RepetitionContentTypeEnum.BASE.value,
    )
    count_repetition = Column(Integer, default=0)
    date_repetition = Column(
        Integer,
        nullable=False,
        default=lambda: calc_date_repetition(),
    )
    slugs = relationship(
        "SlugRepetitionSQL",
        back_populates="repetitions",
        primaryjoin="RepetitionSQL.id == repetition_slug_association.c.repetition_id",
        secondaryjoin="SlugRepetitionSQL.id == repetition_slug_association.c.slug_id",
        secondary=repetition_slug_association,
    )
    title = Column(String, nullable=False, unique=True)
    user_id = Column(String, nullable=False)
    date_last_repetition = Column(Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": RepetitionContentTypeEnum.BASE.value,
        "polymorphic_on": content_type,
    }
