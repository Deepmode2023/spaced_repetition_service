from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.commands import create_word_repetition
from app.application.queries.get_all_repetition import get_all_repetition
from app.schemas.repeptition import (
    CreateFileRepetitionRequest,
    CreateWordRepetitionRequest,
)
from app.schemas.response import RepetitionSchemaResponse
from app.application.http.exception import HTTPExceptionResponse

from .date_type import OptionalQueryDateType, RequiredQueryDateType
from .dependencies import auth_marker, session

with_auth_repetition_route = APIRouter(
    prefix="/repetition",
    tags=["Repetition"],
    # dependencies=[Depends(auth_marker)],
)

repetition_route = APIRouter(prefix="/repetition", tags=["Repetition"])


@repetition_route.get("/", response_model=RepetitionSchemaResponse)
async def get_repetition(
    start_date: OptionalQueryDateType,
    end_date: RequiredQueryDateType,
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
):
    try:
        repetitions = await get_all_repetition(
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
        )
        return RepetitionSchemaResponse(
            status=200,
            details="Successfull",
            model=repetitions,
        )
    except Exception as e:
        return HTTPExceptionResponse(e).response


@with_auth_repetition_route.post(
    "/create_repetition/word",
    response_model=RepetitionSchemaResponse,
)
async def create_word(
    request: CreateWordRepetitionRequest,
):
    try:
        created_repetition = await create_word_repetition(**request.model_dump())

        return RepetitionSchemaResponse(
            status=200,
            details="Successfull",
            model=created_repetition.to_json,
        )
    except Exception as e:
        return HTTPExceptionResponse(e).response


@with_auth_repetition_route.post("/create_repetition/file")
async def create_file_repetition(
    request: CreateFileRepetitionRequest,
):
    pass
