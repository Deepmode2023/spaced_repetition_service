from abc import ABC, abstractmethod

from app.domain.common.vo import URL


class IDocumentRepository(ABC):

    @abstractmethod
    async def save(self, content: bytes, filename: str) -> URL: ...

    @abstractmethod
    async def delete(self, url: URL) -> None: ...

    @abstractmethod
    async def update(self, content: bytes, url: URL) -> URL: ...
