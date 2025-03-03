from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.infrastucture.db.base import Base


class MD(Base):
    __tablename__ = "mds"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tags = relationship("Tag", back_populates="md", cascade="all, delete-orphan")

    def __repr__(self):
        return f"MDRepetition(id={self.id})"
