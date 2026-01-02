from dataclasses import dataclass
from app.domain.vo import RepetitionStatusEnum
import pendulum
from app.domain.utils import repetition_formula
from app.domain.common.exceptions import UnknownFieldInsideEnum


@dataclass
class RepetitionScheduler:
    @staticmethod
    def calculate_next_date(
        count_repetition: int = 0,
        repetition_status: RepetitionStatusEnum = RepetitionStatusEnum.STARTING,
        date_repetition: int = int(pendulum.now().timestamp()),
    ) -> int:
        repetition_time_in_seconds = repetition_formula(count_repetition)
        match repetition_status:
            case RepetitionStatusEnum.STARTING | RepetitionStatusEnum.SUCCESSFUL:
                return date_repetition + repetition_time_in_seconds
            case RepetitionStatusEnum.UNSUCCESSFUL:
                return date_repetition - repetition_time_in_seconds
            case _:
                raise UnknownFieldInsideEnum(enum=RepetitionStatusEnum)
