from fastapi import File, Form, UploadFile
from pydantic import BaseModel

from app.domain.models import LanguageEnum, PartOfSpeachEnum


class CreateFileRepetitionRequest(BaseModel):
    user_id: str
    title: str
    document: UploadFile = File(...)
    document_variant: str


class CreateWordRepetitionRequest(BaseModel):
    user_id: str
    word: str
    synonyms: list[str]
    part_of_speech: PartOfSpeachEnum
    examples: list[str]
    possible_options: list[str]
    context: str
    language: LanguageEnum
    translate: list[str]
    slugs: list[str]
