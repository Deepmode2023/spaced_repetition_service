from sqlalchemy import Column, ForeignKey, Table, Integer

from app.infrastucture.db.base import Base

repetition_slug_association = Table(
    "repetition_slug_association",
    Base.metadata,
    Column("repetition_id", Integer, ForeignKey("repetitions.id")),
    Column("slug_id", Integer, ForeignKey("slug_repetitions.id")),
)
