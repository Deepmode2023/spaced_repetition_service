from app.infrastucture.db.session import get_session

from app.domain.models import Repetition
from app.domain.models.type import DateType
from app.infrastucture.repositories.sqlalchemy import SQLAlchemyRepetitionRepository


async def get_all_repetition(
    start_date: DateType,
    end_date: DateType,
    limit: int,
    offset: int,
) -> list[dict[str, any]]:
    async with get_session() as session:
        dao = SQLAlchemyRepetitionRepository(session=session)
        scalar_result: list[Repetition] = await dao.get_all_repetitions(
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
        )
        return scalar_result
