from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.infrastucture.db.base import Base
from app.infrastucture.db.base import ClassArgument
from ..association import repetition_slug_association
from pydantic import BaseModel


class SlugRepetition(Base):
    """
    A class representing a model for handling `Slug` in the database.

    This model is used to store unique slugs that can be associated with one or more `Repetition` entities.
    Each slug consists of a name (`name`), field must be unique.

    Attributes:
        __tablename__ (str): The name of the table in the database (“slug_repetitions”).

        id (Column): The unique identifier of the slug in UUID format.
                     Type: String (36 characters), automatically generated by uuid4().

        name (Column): The unique name of the slug.
                       Type: String, unique value.

        repetitions (relationship): A many-to-many relationship with the `Repetition` entity.
                                    Describes which repetitions (`Repetition`) use this slug.

    Methods:
        to_json (property): Represents the `SlugRepetition` entity as a JSON dictionary.

            Returns:
                `dict`: A dictionary with the keys `id`, `language` and `name`.

    Example Usage:
        Creating a new slug:
            >>> slug = SlugRepetition(name=“basic”)
            >>> session.add(slug)
            >>> session.commit()

    Convert to JSON:
            >>> print(slug.to_json)
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "basic"
            }
    """

    __tablename__ = "slug_repetitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, unique=True)
    repetitions = relationship(
        "Repetition",
        secondary=repetition_slug_association,
        primaryjoin="SlugRepetition.id == repetition_slug_association.c.slug_id",
        secondaryjoin="Repetition.id == repetition_slug_association.c.repetition_id",
        back_populates="slugs",
    )

    def __repr__(self):
        return f"SlugRepetition(id={self.id}, name={self.name})"

    @classmethod
    def cls_arguments(cls):
        return [ClassArgument(field="name", nullable=False)]

    @property
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class SlugRepetitionSchema(BaseModel):
    id: str
    name: str
