from .repetition import Repetition
from app.domain.common.models import ClassArgument
from app.domain.vo import PartOfSpeachEnum, LanguageEnum
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class WordRepetition(Repetition):
    word: str
    part_of_speech: PartOfSpeachEnum

    examples: list[str] = field(default_factory=list)
    translate: list[str] = field(default_factory=list)
    synonyms: list[str] = field(default_factory=list)
    language: LanguageEnum = field(default=LanguageEnum.ENGLISH_BR)
    context: Optional[str] = field(default=None)
    possible_options: list[str] = field(default_factory=list)
    image_url: Optional[str] = field(default=None)

    def __repr__(self):
        return f"WordRepetition(id={self.id}, word={self.word})"

    @property
    def to_json(self):
        return {
            "id": self.id,
            "word": self.word,
            "translate": self.translate,
            "synonyms": self.synonyms,
            "part_of_speech": self.part_of_speech,
            "examples": self.examples,
            "language": self.language,
            "context": self.context,
            "possible_options": self.possible_options,
            "image_url": self.image_url,
            **super().to_json,
        }

    @classmethod
    def cls_arguments(cls) -> list[ClassArgument]:
        return [
            ClassArgument(field="word", nullable=False),
            ClassArgument(field="translate", nullable=True),
            ClassArgument(field="synonyms", nullable=True),
            ClassArgument(field="part_of_speech", nullable=True),
            ClassArgument(field="examples", nullable=True),
            ClassArgument(field="language", nullable=True),
            ClassArgument(field="context", nullable=True),
            ClassArgument(field="possible_options", nullable=True),
            ClassArgument(field="image_url", nullable=True),
            *super().cls_arguments(),
        ]
