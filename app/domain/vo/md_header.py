from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class MDHeader:
    url: str
    highlights: list[str] = field(default_factory=list)
    hints: list[str] = field(default_factory=list)
    load_links: list[UUID] = field(default_factory=list)
    importants: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    uniq_link: UUID | None = None

    def set_hint(self, hint: str) -> None:
        self.hints.append(hint)

    def set_load_link(self, link: str | UUID) -> None:
        self.load_links.append(self._to_uuid(link))

    def set_important(self, important: str) -> None:
        self.importants.append(important)

    def set_tag(self, tag: str) -> None:
        self.tags.append(tag)

    def set_uniq_link(self, uniq_link: str | UUID) -> None:
        if self.uniq_link is not None:
            raise ValueError("`uniq_link` field already exists")
        self.uniq_link = self._to_uuid(uniq_link)

    def _to_uuid(self, value: str | UUID) -> UUID:
        if isinstance(value, UUID):
            return value
        return UUID(value)
