from .repetition import Repetition
from app.domain.common.models import ClassArgument
from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class MDRepetition(Repetition):
    url: str
    highlights: tuple[str, ...] = field(default_factory=tuple)
    hints: tuple[str, ...] = field(default_factory=tuple)
    load_links: tuple[UUID, ...] = field(default_factory=tuple)
    importants: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=list)
    uniq_link: UUID | None = None

    def __repr__(self):
        return f"MDRepetition(id={self.id}, url={self.url})"

    @property
    def to_json(self):
        return {
            "id": self.id,
            "url": self.url,
            "highlights": self.highlights,
            "hints": self.hints,
            "load_links": self.load_links,
            "importants": self.importants,
            "tags": self.tags,
            "uniq_link": self.uniq_link,
            **super().to_json,
        }

    @classmethod
    def cls_arguments(cls) -> list[ClassArgument]:
        return [
            ClassArgument(field="url", nullable=False),
            ClassArgument(field="highlights", nullable=False),
            ClassArgument(field="hints", nullable=False),
            ClassArgument(field="load_links", nullable=False),
            ClassArgument(field="importants", nullable=False),
            ClassArgument(field="tags", nullable=False),
            ClassArgument(field="uniq_link", nullable=True),
            *super().cls_arguments(),
        ]
