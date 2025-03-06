from enum import Enum
from typing import Annotated, Union

from uuid import uuid4

import pendulum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship

from pydantic import BaseModel, Field
from .word.word_repetition import WordRepetitionSchema

from app.infrastucture.db.base import Base
from .enum import EnumABC

from ..utils import repetition_formula
from .association import repetition_slug_association
from .word.word_repetition import LanguageEnum, PartOfSpeachEnum, WordRepetition
from ..exceptions import UnknownFieldInsideEnum


class RepetitionStatusEnum(EnumABC):
    SUCCESSFUL = 1
    UNSUCCESSFUL = 0
    STARTING = -1

    @classmethod
    def fields(cls):
        """
        Returns all fields of the enum as a dictionary.

        Returns:
            dict: A dictionary with enum names as keys and values as enum values.
        """
        return {item.name: item.value for item in cls}

    @property
    def get_name(self):
        return "repetitionstatusenum"


class RepetitionContentTypeEnum(EnumABC):
    FILE = "file"
    WORD = "word"
    TEXT = "text"

    @classmethod
    def fields(cls):
        """
        Returns all fields of the enum as a dictionary.

        Returns:
            dict: A dictionary with enum names as keys and values as enum values.
        """
        return {item.name: item.value for item in cls}

    @property
    def get_name(self):
        return "repetitioncontenttypeenum"


class Repetition(Base):
    """
    Repetition

    The `Repetition` class is a database model designed to manage and track repetitions for different types of content, such as words, files, and texts.
    It includes attributes for repetition tracking and methods for retrieving related content and exporting data in JSON format.

    Attributes:
        id (String, Primary Key):
            A unique identifier for each repetition instance, generated using `uuid4`.

        user_id (String, nullable=False):
                The unique identifier of the associated user

        title (String, uniq):
                The title of the repetition

        slugs (Array[String]):
                List of associated slugs

        content_type (String, Required):
            Specifies the type of content associated with the repetition.
            Possible values are defined in `RepetitionContentTypeEnum` (e.g., WORD, FILE, TEXT).

        content_id (String, Required):
            A unique identifier for the associated content, linked based on the `content_type`.

        count_repetition (Integer, Default: 0):
            Tracks the number of times the content has been repeated.

        date_repetition (Integer, Required):
            A timestamp representing the next scheduled repetition.
            Defaults to the current timestamp using `calc_date_repetition`.

        date_last_repetition (Integer, Optional):
            A timestamp for the last repetition of the content, or `None` if no repetition has occurred yet.

    Properties:
        content:
            Retrieves the associated content object based on the `content_type` and `content_id`.

            Returns:
                - For `content_type == WORD`: Fetches the `WordRepetition` object using the database session.
                - For `content_type == FILE` or `TEXT`: Currently returns `None`.
                - Raises `UnknownFieldInsideEnum` if the `content_type` is not recognized in `RepetitionContentTypeEnum`.

            Exceptions:
                - `UnknownFieldInsideEnum`: Raised when an invalid `content_type` is encountered.

        to_json:
            Exports the object's data as a JSON-compatible dictionary.

            Returns:
                A dictionary with the following fields:
                    - `id`
                    - `slugs`
                    - `title`
                    - `user_id`
                    - `content_type`
                    - `content_id`
                    - `count_repetition`
                    - `date_repetition`
                    - `date_last_repetition`
                If the `content` has a `to_json` method, its data is also included in the dictionary.
    """

    __tablename__ = "repetitions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    content_type = Column(
        SQLEnum(
            RepetitionContentTypeEnum,
            name="contenttypeenum",
            create_type=False,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    )
    content_id = Column(String(36), nullable=False)
    count_repetition = Column(Integer, default=0)
    date_repetition = Column(
        Integer,
        nullable=False,
        default=lambda: calc_date_repetition(),
    )
    slugs = relationship(
        "SlugRepetition",
        back_populates="repetitions",
        primaryjoin="Repetition.id == repetition_slug_association.c.repetition_id",
        secondaryjoin="SlugRepetition.id == repetition_slug_association.c.slug_id",
        secondary=repetition_slug_association,
    )
    title = Column(String, nullable=False, unique=True)
    user_id = Column(String, nullable=False)
    date_last_repetition = Column(Integer, nullable=True)

    @property
    def content(self):
        """
        Retrieves the associated content object based on the `content_type` and `content_id`.

        The method uses a dictionary-based dispatcher to map `content_type` to specific
        content-fetching logic. If the `content_type` is unrecognized, an exception is raised.

        Returns:
            - If `content_type == RepetitionContentTypeEnum.WORD`: Fetches the `WordRepetition` object
            using the database session.
            - If `content_type == FILE` or `TEXT`: Returns `None`.

        Raises:
            UnknownFieldInsideEnuRepetitionContentTypeEnumm: Raised if the `content_type` is not recognized in
            `RepetitionContentTypeEnum`.
        """
        from ..exceptions import UnknownFieldInsideEnum

        content_fetcher = {
            RepetitionContentTypeEnum.WORD: lambda: self.session.query(
                WordRepetition
            ).get(self.content_id),
            RepetitionContentTypeEnum.FILE: lambda: None,
            RepetitionContentTypeEnum.TEXT: lambda: None,
        }
        try:
            return content_fetcher[self.content_type]()
        except KeyError:
            raise UnknownFieldInsideEnum(
                enum=RepetitionContentTypeEnum,
            )

    def __repr__(self):
        return f"Repetition(content_type={self.content_type}, title={self.title}, day_repetition={self.date_repetition}"

    @property
    def to_json(self):
        """
        Exports the object's data as a JSON-compatible dictionary.

        The method retrieves all relevant attributes and dynamically includes additional data
        from the associated content object if it supports the `to_json` method.

        Returns:
            dict: A dictionary containing:
                - `id`
                - `content_type`
                - `content_id`
                - `count_repetition`
                - `date_repetition`
                - `date_last_repetition`
                - `user_id`
                - `title`
                - `slugs`

            If the associated `content` has a `to_json` method, its data is merged into the dictionary.
        """
        unpacking_slugs = [
            slug.to_json if hasattr(slug, "to_json") else slug for slug in self.slugs
        ]

        data = {
            "id": self.id,
            "content_type": self.content_type,
            "content_id": self.content_id,
            "count_repetition": self.count_repetition,
            "date_repetition": self.date_repetition,
            "date_last_repetition": self.date_last_repetition,
            "title": self.title,
            "slugs": unpacking_slugs,
            "user_id": self.user_id,
        }
        if hasattr(self.content, "to_json"):
            data.update({"deps_model": self.content.to_json})

        return data

    def update_repetition_schedule(
        self,
        repetition_status: RepetitionStatusEnum,
    ):
        """
        Updates the repetition schedule and counters based on the provided status.

        This method adjusts the `count_repetition` and calculates the next repetition time
        (`date_repetition`) using the `repetition_formula` function. The update depends on whether
        the repetition was successful or not.

        Args:
            repetition_status (RepetitionStatusEnum): The status of the repetition. Must be a valid
            value from `RepetitionStatusEnum`.

        Raises:
            ValueError: Raised if `repetition_status` is not a valid member of `RepetitionStatusEnum`.

        Behavior:
            - Updates `date_last_repetition` to the current timestamp.
            - Adjusts `count_repetition`:
                - Increments by 1 if the status is SUCCESSFUL.
                - Decrements by 1 if the status is unsuccessful, ensuring it doesn't fall below 0.
            - Calculates the next repetition time in seconds using `repetition_formula`.
            - Updates `date_repetition` based on the repetition status:
                - Adds the calculated time if SUCCESSFUL.
                - Subtracts the calculated time if unsuccessful.
        """
        if repetition_status not in RepetitionStatusEnum:
            raise UnknownFieldInsideEnum(enum=RepetitionStatusEnum)

        self.date_last_repetition = int(pendulum.now().timestamp())
        self.count_repetition = max(
            0,
            (
                self.count_repetition + 1
                if RepetitionStatusEnum.SUCCESSFUL
                else self.count_repetition - 1
            ),
        )
        self.date_repetition = calc_date_repetition(
            count_repetition=self.count_repetition,
            repetition_status=repetition_status,
            date_repetition=self.date_repetition,
        )


def calc_date_repetition(
    count_repetition: int = 0,
    repetition_status: RepetitionStatusEnum = RepetitionStatusEnum.STARTING,
    date_repetition: int = pendulum.now().timestamp(),
) -> int:
    repetition_time_in_seconds = repetition_formula(count_repetition)
    match repetition_status:
        case RepetitionStatusEnum.STARTING | RepetitionStatusEnum.SUCCESSFUL:
            return date_repetition + repetition_time_in_seconds
        case RepetitionStatusEnum.UNSUCCESSFUL:
            return date_repetition - repetition_time_in_seconds
        case _:
            raise UnknownFieldInsideEnum(enum=RepetitionStatusEnum)


class RepetitionWordSchema(BaseModel):
    id: str
    content_type: RepetitionContentTypeEnum
    content_id: str
    count_repetition: int
    date_repetition: int
    slugs: int
    title: str
    user_id: str
    date_last_repetition: int
    deps_model: WordRepetitionSchema
