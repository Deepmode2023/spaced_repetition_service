from dataclasses import dataclass
from typing import List

import pendulum
from sqlalchemy import ChunkedIteratorResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import (
    RepetitionAggragetion,
    RepetitionContentTypeEnum,
    RepetitionStatusEnum,
)
from app.domain.models.type import DateType
from app.domain.repositories.repetition import RepetitionRepository
from app.domain.services.repetition import RepetitionServices


@dataclass(
    eq=False,
    frozen=True,
    kw_only=True,
)
class SQLAlchemyRepetitionRepository(RepetitionRepository):
    session: AsyncSession
    services = RepetitionServices()

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
        self,
        type_repetition: RepetitionContentTypeEnum,
        **kwargs,
    ):
        repetition: RepetitionAggragetion = await self.services.create_repetition(
            type_repetition=type_repetition,
            **kwargs,
        )

        print(repetition)

    async def successful_repetition(id):
        pass

    async def unsuccessful_repetition(id):
        pass
