from ..schemas import CreateFileRepetitionRequest
from app.domain.entities import MDRepetition
from app.domain.repository import IRepetitionRepository, IDocumentRepository


async def create_md_repetition(
    repetition: CreateFileRepetitionRequest,
    document: bytes,
    rep_repository: IRepetitionRepository,
    doc_repetition: IDocumentRepository,
) -> MDRepetition:
    document_link = doc_repetition.save(document)
    md_repetition = await rep_repository.create_md_repetition(
        document_link=document_link,
        title=repetition.title,
        slugs=repetition.slugs,
        user_id=repetition.user_id,
    )

    return md_repetition
