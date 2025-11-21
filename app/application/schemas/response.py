from typing import TypeVar, Generic, Union, Annotated, List, Optional
from pydantic import BaseModel
from uuid import UUID
from app.domain.models import SlugRepetition, RepetitionContentTypeEnum, Repetition

T = TypeVar("T")


class TotalResponse(BaseModel, Generic[T]):
    status: int
    details: str
    model: T | List


RepetitionSchemaResponse = Annotated[
    Union[
        TotalResponse["RepetitionResponse"],
        TotalResponse["RepetitionResponse"],
    ],
    "RepetitionSchema",
]


class RepetitionResponse(BaseModel):
    id: UUID
    title: str
    hint: str
    user_id: UUID
    date_last_repetition: Optional[int]
    count_repetition: int
    date_repetition: int
    slugs: list[SlugRepetition]

    @classmethod
    def from_domain(cls, rep: Repetition):
        return cls(
            id=rep.id,
            title=rep.title,
            hint=rep.hint,
            user_id=rep.user_id,
            date_last_repetition=rep.date_last_repetition,
            count_repetition=rep.count_repetition,
            date_repetition=rep.date_repetition,
            slugs=rep.slugs,
        )
