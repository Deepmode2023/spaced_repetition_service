from typing import TypeVar, Generic, Union, Annotated, List
from app.domain.models import WordRepetitionSchema
from pydantic import BaseModel

T = TypeVar("T")


class TotalResponse(BaseModel, Generic[T]):
    status: int
    details: str
    model: T | List


RepetitionSchemaResponse = Annotated[
    Union[
        TotalResponse[WordRepetitionSchema],
        TotalResponse[WordRepetitionSchema],
    ],
    "RepetitionSchema",
]
