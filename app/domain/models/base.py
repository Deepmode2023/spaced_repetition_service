from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import declared_attr, relationship

from app.infrastucture.db.base import Base

from .association import repetition_slug_association


class RepetitionBase(Base):
    __abstract__ = True
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))

    @declared_attr
    def slugs(cls):
        return relationship(
            "SlugRepetition",
            back_populates="repetition",
            secondary=repetition_slug_association,
        )

    title = Column(String, nullable=False, unique=True)
    user_id = Column(String, nullable=False)

    def __repr__(self):
        """
        String representation of the `Repetition` object.

        Returns:
            str: A string that represents the `Repetition` object in the format:
                 "Repetition(id=<id>, title=<title>)"
        """
        return f"Repetition(id={self.id}, title={self.title})"

    def __eq__(self, other):
        """
        Equality check between two `Repetition` objects.

        Args:
            other (Repetition): The `Repetition` object to compare with.

        Returns:
            bool: True if the two `Repetition` objects are equal, False otherwise.
        """
        if isinstance(other, RepetitionBase):
            return self.title == other.title and self.user_id == other.user_id
        return False

    @property
    def to_json(self):
        """
        Converts the `Repetition` object to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representation of the `Repetition` object with the following fields:
                  - `id`: The unique identifier of the repetition.
                  - `title`: The title of the repetition.
                  - `slugs`: List of associated slugs.
                  - `user_id`: The unique identifier of the associated user.
        """
        return {
            "id": self.id,
            "title": self.title,
            "slugs": self.slugs,
            "user_id": self.user_id,
        }
