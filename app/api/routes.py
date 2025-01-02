from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.queries.get_all_repetition import get_all_repetition

from .date_type import OptionalQueryDateType, RequiredQueryDateType
from .dependencies import session

repetition_route = APIRouter(prefix="/repetition", tags=["Repetition"])


@repetition_route.get("/")
async def get_repetition(
    start_date: OptionalQueryDateType,
    end_date: RequiredQueryDateType,
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
    session: AsyncSession = Depends(session),
):
    return await get_all_repetition(
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
        session=session,
    )
