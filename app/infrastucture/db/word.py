from .base import Base
from sqlalchemy import (
    ARRAY,
    Column,
    String,
    Enum as SQLEnum,
    ForeignKeyConstraint,
    ForeignKey,
)
from app.domain.models import PartOfSpeachEnum, LanguageEnum, RepetitionContentTypeEnum


class WordRepetitionSQL(Base):
    __tablename__ = "word_repetitions"
    id = Column(
        String(36),
        ForeignKey("repetitions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    word = Column(String, unique=True, nullable=False)
    translate = Column(ARRAY(String), nullable=True)
    synonyms = Column(ARRAY(String), nullable=True)
    part_of_speech = Column(
        SQLEnum(
            PartOfSpeachEnum,
            name=PartOfSpeachEnum.get_name(),
            create_type=False,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=True,
    )
    examples = Column(ARRAY(String), nullable=True)
    language = Column(
        SQLEnum(
            LanguageEnum,
            name=LanguageEnum.get_name(),
            create_type=False,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=LanguageEnum.ENGLISH_BR,
    )
    context = Column(String, nullable=True)
    possible_options = Column(ARRAY(String), nullable=True)
    image_url = Column(String, nullable=True)

    table_args__ = (
        ForeignKeyConstraint(
            ["id"], ["repetitions.id"], name="fk_word_repetitions_repetition_id"
        ),
    )

    __mapper_args__ = {
        "polymorphic_identity": RepetitionContentTypeEnum.WORD.value,
    }

    def __repr__(self):
        return f"WordRepetition(id={self.id}, word={self.word})"
