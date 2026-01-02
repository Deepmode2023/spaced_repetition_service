import pendulum
from app.domain.common.models import ClassArgument
from typing import Optional
from app.domain.vo import RepetitionContentTypeEnum, RepetitionStatusEnum
from app.domain.common.exceptions import UnknownFieldInsideEnum
from .slug import SlugRepetition
from app.domain.common.utils.snowflake import seq
from app.domain.services.repetition_scheduler import RepetitionScheduler


class Repetition:
    title: str
    hint: str
    user_id: int
    id: int
    date_last_repetition: Optional[int]
    content_type: RepetitionContentTypeEnum
    count_repetition: int
    date_repetition: int
    slugs: list[SlugRepetition]

    def __init__(
        self,
        title: str,
        hint: str,
        user_id: int,
        id: Optional[int] = lambda: next(seq),
        date_last_repetition: Optional[int] = None,
        content_type: RepetitionContentTypeEnum = RepetitionContentTypeEnum.BASE,
        count_repetition: int = 0,
        date_repetition: Optional[int] = None,
        slugs: list[SlugRepetition] = [],
    ):
        self.title = title
        self.hint = hint
        self.user_id = user_id
        self.id = id
        self.date_last_repetition = date_last_repetition
        self.content_type = content_type
        self.count_repetition = count_repetition
        self.slugs = slugs

        if date_repetition is None:
            date_repetition = RepetitionScheduler.calculate_next_date()
        self.date_repetition = date_repetition

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
                - `count_repetition`
                - `date_repetition`
                - `date_last_repetition`
                - `user_id`
                - `title`
                - `slugs`
                - `hint`

            If the associated `content` has a `to_json` method, its data is merged into the dictionary.
        """
        unpacking_slugs = [
            slug.to_json if hasattr(slug, "to_json") else slug for slug in self.slugs
        ]

        return {
            "id": self.id,
            "content_type": self.content_type,
            "count_repetition": self.count_repetition,
            "date_repetition": int(self.date_repetition),
            "date_last_repetition": (
                int(self.date_last_repetition) if self.date_last_repetition else None
            ),
            "title": self.title,
            "slugs": unpacking_slugs,
            "user_id": self.user_id,
            "hint": self.hint,
        }

    @classmethod
    def cls_arguments(cls) -> list[ClassArgument]:
        return [
            ClassArgument(field="content_type", nullable=False),
            ClassArgument(field="title", nullable=False),
            ClassArgument(field="slugs", nullable=False),
            ClassArgument(field="user_id", nullable=False),
            ClassArgument(field="hint", nullable=False),
        ]

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

        self.date_last_repetition = pendulum.now().timestamp()
        self.count_repetition = max(
            0,
            (
                self.count_repetition + 1
                if RepetitionStatusEnum.SUCCESSFUL
                else self.count_repetition - 1
            ),
        )
        self.date_repetition = RepetitionScheduler.calculate_next_date(
            count_repetition=self.count_repetition,
            repetition_status=repetition_status,
            date_repetition=self.date_repetition,
        )
