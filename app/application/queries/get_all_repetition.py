from dataclasses import dataclass
from app.domain.repository.repetition import IRepetitionRepository
from app.domain.entities import Repetition
from app.domain.common.vo import DateType


@dataclass(frozen=True, slots=True)
class GetAllRepetitionQuery:
    start_date: DateType
    end_date: DateType
    limit: int
    offset: int


@dataclass
class GetAllRepetitionHandler:
    repo: IRepetitionRepository

    async def handle(self, query: GetAllRepetitionQuery) -> list[Repetition]:
        return await self.repo.get_all_repetitions(
            start_date=query.start_date,
            end_date=query.end_date,
            limit=query.limit,
            offset=query.offset,
        )
