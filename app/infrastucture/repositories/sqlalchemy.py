from dataclasses import dataclass
from typing import List

import pendulum
from sqlalchemy import ChunkedIteratorResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import (
    Repetition,
    RepetitionContentTypeEnum,
    RepetitionStatusEnum,
    WordRepetition,
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
    ) -> List[Repetition]:

        stmp = (
            select(Repetition)
            .where(
                Repetition.date_repetition.between(
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
        title: str,
        user_id: str,
        slugs: list[str],
        **kwargs,
    ):
        try:
            dependency_repetition_model = (
                self.services.create_dependency_repetition_model(
                    content_type=content_type,
                    **kwargs,
                )
            )

            self.session.add(dependency_repetition_model)
            await self.session.flush()

            repetition_model: Repetition = self.services.create_repetition_model(
                content_type=content_type,
                title=title,
                dependency_repetition=dependency_repetition_model,
                user_id=user_id,
                slugs=slugs,
            )

            self.session.add(repetition_model)
            await self.session.flush()

            await self.session.commit()

            return repetition_model
        except Exception as ex:
            print(ex)

    async def successful_repetition(id):
        pass

    async def unsuccessful_repetition(id):
        pass
