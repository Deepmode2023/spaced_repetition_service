from .base import Base
from sqlalchemy import (
    ARRAY,
    Column,
    String,
    ForeignKeyConstraint,
    ForeignKey,
    Integer,
    UUID,
)

from app.domain.vo import RepetitionContentTypeEnum


class MDRepetitionSQL(Base):
    __tablename__ = "md_repetitions"
    id = Column(
        Integer,
        ForeignKey("repetitions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    url = Column(String, unique=True, nullable=False)
    highlights = Column(ARRAY(String), nullable=True)
    hints = Column(ARRAY(String), nullable=True)
    load_links = Column(ARRAY(String), nullable=True)
    importants = Column(ARRAY(String), nullable=True)
    uniq_link = Column(UUID, nullable=False)

    table_args__ = (
        ForeignKeyConstraint(
            ["id"], ["repetitions.id"], name="fk_word_repetitions_repetition_id"
        ),
    )

    __mapper_args__ = {
        "polymorphic_identity": RepetitionContentTypeEnum.MD.value,
    }

    def __repr__(self):
        return f"MDRepetition(id={self.id}, word={self.uniq_link})"
