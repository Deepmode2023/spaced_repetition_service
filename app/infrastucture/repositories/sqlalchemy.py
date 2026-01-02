from dataclasses import dataclass
from typing import List

from sqlalchemy import ChunkedIteratorResult, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastucture.exceptions.sqlalchemy import DuplicateAddedEntity
from sqlalchemy.orm import with_polymorphic, selectinload

from app.domain.vo import (
    RepetitionContentTypeEnum,
    RepetitionStatusEnum,
)
from app.domain.entities import Repetition, WordRepetition
from app.infrastucture.db.repetition import RepetitionSQL
from app.domain.common.vo import DateType
from app.domain.repository.repetition import IRepetitionRepository
from app.application.repetition import RepetitionServices
from app.domain.common.utils import SieveValueErrorExceptionExternal


@dataclass(eq=False, frozen=True, kw_only=True)
class SQLAlchemyRepetitionRepository(IRepetitionRepository):
    session: AsyncSession
    services = RepetitionServices()

    async def get_all_repetitions(
        self,
        start_date: DateType,
        end_date: DateType,
        limit: int,
        offset: int,
    ) -> List[WordRepetition]:
        RepetitionPolymorphic = with_polymorphic(RepetitionSQL, "*", aliased=True)
        stmp = (
            select(RepetitionPolymorphic)
            .options(selectinload(RepetitionPolymorphic.slugs))
            .where(
                RepetitionPolymorphic.date_repetition.between(
                    start_date.timestamp, end_date.timestamp
                )
            )
            .limit(limit)
            .offset(offset)
        )
        result: ChunkedIteratorResult = await self.session.execute(stmp)
        return result.scalars().all()

    async def update_repetition(
        repetition_id,
        title=None,
        description=None,
        document_link=None,
        slug=None,
    ) -> Repetition:
        pass

    async def create_repetition(
        self,
        content_type: RepetitionContentTypeEnum,
        **kwargs,
    ):
        try:
            repetition_model = self.services.create_repetition_model(
                content_type=content_type,
                **kwargs,
            )

            self.session.add(repetition_model)
            await self.session.commit()

            return repetition_model

        except IntegrityError:
            await self.session.rollback()
            raise DuplicateAddedEntity(
                fields=[
                    *kwargs.keys(),
                    "title",
                    "user_id",
                    "slugs",
                    "content_type",
                ]
            )
        except SieveValueErrorExceptionExternal:
            raise

    async def successful_repetition(id):
        pass

    async def unsuccessful_repetition(id):
        pass
