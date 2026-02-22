import pendulum
from typing import Optional
from functools import partial

from app.domain.vo import RepetitionContentTypeEnum, RepetitionStatusEnum
from app.domain.common.models import ClassArgument
from app.domain.common.exceptions import UnknownFieldInsideEnum, WrongIDType
from .slug import SlugRepetition
from app.domain.common.utils.snowflake import seq, is_snowflake_id
from app.domain.utils import repetition_formula


class Repetition:
    title: str
    user_id: int
    id: int
    content_type: RepetitionContentTypeEnum
    slugs: list[SlugRepetition]
    hint: str | None
    _count_repetition: int
    _date_repetition: int
    _date_last_repetition: int | None

    def __init__(
        self,
        title: str,
        user_id: int,
        id: Optional[int] = None,
        slugs: Optional[list[SlugRepetition]] = None,
        hint: Optional[str] = None,
        count_repetition: Optional[int] = None,
        date_last_repetition: Optional[int] = None,
        content_type: RepetitionContentTypeEnum = RepetitionContentTypeEnum.BASE,
        date_repetition: Optional[int] = None,
    ):
        self.id = id if id and self._invariant_id(id) else next(seq)
        self.title = title
        self.hint = hint
        self.user_id = self._invariant_id(user_id)
        self.content_type = content_type
        self.slugs = slugs or []
        self._date_last_repetition = date_last_repetition
        self._count_repetition = count_repetition or 0
        self._date_repetition = date_repetition
        if self._date_repetition is None:
            self._date_repetition = self._calculate_next_date(
                RepetitionStatusEnum.STARTING
            )

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str):
            raise ValueError("You pass incorect type for `title`. Must be String type")
        if not len(value) > 0:
            raise ValueError("The title must contains more than 1 chars.")
        self._title = value

    @property
    def date_last_repetition(self):
        return self._date_last_repetition

    @date_last_repetition.setter
    def date_last_repetition(self, value: int):
        if not isinstance(value, int) and len(value) != 10:
            raise ValueError(
                "You pass incorect timestamp for `date_last_repetition`. Need to be 10 char int"
            )
        self._date_last_repetition = value

    @property
    def count_repetition(self):
        return self._count_repetition

    @count_repetition.setter
    def count_repetition(self, value: int):
        if value < 0:
            raise ValueError("`count_repetition` must be grather than 0")

        self._count_repetition = value

    @property
    def date_repetition(self):
        return self._date_repetition

    @date_repetition.setter
    def date_repetition(self, value: int):
        if not isinstance(value, int) and len(value) != 10:
            raise ValueError(
                "You pass incorect timestamp for `date_repetition`. Need to be 10 char int"
            )
        self._date_repetition = value

    @staticmethod
    def _invariant_id(id: int) -> int:
        if is_snowflake_id(id):
            return id

        raise WrongIDType()

    def __repr__(self):
        return f"Repetition(content_type={self.content_type}, title={self.title}, date_repetition={self.date_repetition})"

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
            "count_repetition": self._count_repetition,
            "date_repetition": int(self._date_repetition),
            "date_last_repetition": (
                int(self._date_last_repetition) if self._date_last_repetition else None
            ),
            "title": self.title,
            "slugs": unpacking_slugs,
            "user_id": self.user_id,
            "hint": self.hint,
        }

    def _handling_status_count_repetition(
        self,
        repetition_status: RepetitionStatusEnum,
    ) -> None:
        count_repetition_partial = partial(max, 0)
        if repetition_status not in RepetitionStatusEnum:
            raise UnknownFieldInsideEnum(enum=RepetitionStatusEnum)

        match repetition_status:
            case RepetitionStatusEnum.SUCCESSFUL:
                self._count_repetition = count_repetition_partial(
                    self._count_repetition + 1
                )
            case RepetitionStatusEnum.UNSUCCESSFUL:
                self._count_repetition = count_repetition_partial(
                    self._count_repetition - 1
                )
            case _:
                self._count_repetition = 0

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

        self._date_last_repetition = pendulum.now().timestamp()

        self._handling_status_count_repetition(repetition_status)
        self._date_repetition = self._calculate_next_date(repetition_status)

    def _calculate_next_date(self, repetition_status: RepetitionStatusEnum) -> int:
        repetition_time_in_seconds = repetition_formula(self._count_repetition)

        ## INVARIANT case with wrong passing date_repetition which less than calculatated time.
        normalize_date_repetition = max(
            self._date_repetition or 0,
            int(pendulum.now().timestamp()),
        )

        match repetition_status:
            case RepetitionStatusEnum.STARTING | RepetitionStatusEnum.SUCCESSFUL:
                return normalize_date_repetition + repetition_time_in_seconds
            case RepetitionStatusEnum.UNSUCCESSFUL:
                return normalize_date_repetition - repetition_time_in_seconds
            case _:
                return normalize_date_repetition
