from sqlalchemy import Column, ForeignKey, String, Table

from app.infrastucture.db.base import Base

synonym_association = Table(
    "synonym_association",
    Base.metadata,
    Column(
        "word_id",
        String(36),
        ForeignKey("word_repetitions.id"),
        primary_key=True,
    ),
    Column(
        "synonym_id",
        String(36),
        ForeignKey("word_repetitions.id"),
        primary_key=True,
    ),
)
