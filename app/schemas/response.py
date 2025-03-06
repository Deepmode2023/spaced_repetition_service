from typing import TypeVar, Generic, Union, Annotated
from app.domain.models import RepetitionWordSchema
from pydantic import BaseModel

T = TypeVar("T")


class TotalResponse(BaseModel, Generic[T]):
    status: int
    details: str
    model: T


RepetitionSchemaResponse = Annotated[
    Union[TotalResponse[RepetitionWordSchema], TotalResponse[RepetitionWordSchema]],
    "RepetitionSchema",
]
