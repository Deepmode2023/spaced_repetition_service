from dataclasses import dataclass
from typing import List

import pendulum
from sqlalchemy import ChunkedIteratorResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import RepetitionAggragetion, RepetitionStatusEnum
from app.domain.models.type import DateType
from app.domain.repositories.repetition_repository import RepetitionRepository


@dataclass(
    eq=False,
    frozen=True,
    kw_only=True,
)
class SQLAlchemyRepetitionRepository(RepetitionRepository):
    session: AsyncSession

    async def get_all_repetitions(
        self,
        start_date: DateType,
        end_date: DateType,
        limit: int,
        offset: int,
    ) -> List[RepetitionAggragetion]:
        stmt = (
            select(RepetitionAggragetion)
            .where(
                RepetitionAggragetion.date_repetition >= start_date.timestamp,
                RepetitionAggragetion.date_repetition <= end_date.timestamp,
            )
            .limit(limit)
            .offset(offset)
        )
        result: ChunkedIteratorResult = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_repetition(
        repetition_id,
        title=None,
        description=None,
        document_link=None,
        slug=None,
    ) -> RepetitionAggragetion:
        pass

    async def create_repetition(
        title,
        user_id,
        description=None,
        document_link=None,
        slug=None,
    ):
        pass

    async def successful_repetition(id):
        pass

    async def unsuccessful_repetition(id):
        pass
