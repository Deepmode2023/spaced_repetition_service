from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.queries.get_all_repetition import get_all_repetition
from app.schemas.create_repeptition import CreateFileRepetitionRequest

from .date_type import OptionalQueryDateType, RequiredQueryDateType
from .dependencies import auth_marker, session

with_auth_repetition_route = APIRouter(
    prefix="/repetition",
    tags=["Repetition"],
    # dependencies=[Depends(auth_marker)],
)

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


@with_auth_repetition_route.post("/create_repetition/simple")
async def create_simple_repetition(
    user_id: str,
    title: str,
    description: str,
):
    pass


@with_auth_repetition_route.post("/create_repetition/file")
async def create_file_repetition(request: CreateFileRepetitionRequest):
    pass
