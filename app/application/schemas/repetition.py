from typing import Optional
from pydantic import BaseModel
from fastapi import Form

from app.domain.vo import LanguageEnum, PartOfSpeachEnum


class RepetitionRequest(BaseModel):
    title: str
    user_id: int
    id: Optional[int] = None
    slugs: list[str]
    hint: Optional[str] = None
    count_repetition: Optional[int] = None
    date_repetition: Optional[int] = None
    date_last_repetition: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        user_id: int = Form(...),
        slugs: list[str] = Form(...),
        id: Optional[int] = Form(None),
        hint: Optional[str] = Form(None),
        count_repetition: Optional[int] = Form(None),
        date_repetition: Optional[int] = Form(None),
        date_last_repetition: Optional[int] = Form(None),
    ):
        return cls(
            title=title,
            user_id=user_id,
            slugs=slugs,
            id=id,
            hint=hint,
            count_repetition=count_repetition,
            date_repetition=date_repetition,
            date_last_repetition=date_last_repetition,
        )


class CreateFileRepetitionRequest(RepetitionRequest):
    pass


class CreateWordRepetitionRequest(RepetitionRequest):
    word: str
    synonyms: list[str]
    part_of_speech: PartOfSpeachEnum
    examples: list[str]
    possible_options: list[str]
    context: str
    language: LanguageEnum
    translate: list[str]
    slugs: list[str]
