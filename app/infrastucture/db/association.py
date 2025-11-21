from sqlalchemy import Column, ForeignKey, String, Table

from app.infrastucture.db.base import Base

repetition_slug_association = Table(
    "repetition_slug_association",
    Base.metadata,
    Column("repetition_id", String(36), ForeignKey("repetitions.id")),
    Column("slug_id", String(36), ForeignKey("slug_repetitions.id")),
)
