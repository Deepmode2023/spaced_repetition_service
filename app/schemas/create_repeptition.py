from fastapi import File, Form, UploadFile
from pydantic import BaseModel


class CreateFileRepetitionRequest(BaseModel):
    user_id: str
    title: str
    document: UploadFile = File(...)
    document_variant: str
