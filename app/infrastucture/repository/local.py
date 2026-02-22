from pathlib import Path
import uuid
import aiofiles

from app.domain.repository import IDocumentRepository
from app.domain.common.vo import URL


class LocalFileRepository(IDocumentRepository):
    def __init__(self, base_dir: Path | None = None, public_prefix: str = "/static"):
        self._base_dir = base_dir or self._init_storage()
        self._public_prefix = public_prefix

    async def save(self, content: bytes, filename: str = "document.md") -> URL:
        file_id = uuid.uuid4().hex
        ext = Path(filename).suffix or ".md"

        file_path = self._base_dir / f"{file_id}{ext}"

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        return self._build_url(file_path)

    async def delete(self, url: URL) -> None:
        file_path = self._resolve_path(url)

        if file_path.exists():
            file_path.unlink()

    async def update(self, content: bytes, url: URL) -> URL:
        file_path = self._resolve_path(url)

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        return url

    def _init_storage(self) -> Path:
        base_dir = Path.cwd() / "static"
        base_dir.mkdir(parents=True, exist_ok=True)
        return base_dir

    def _build_url(self, file_path: Path) -> URL:
        return URL(f"{self._public_prefix}/{file_path.name}")

    def _resolve_path(self, url: URL) -> Path:
        filename = Path(str(url)).name
        return self._base_dir / filename
