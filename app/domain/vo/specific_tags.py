from re import compile, IGNORECASE, Match
from enum import Enum, unique
from .tag import Tag, TagMatch

UUID_PATTERN = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}"


@unique
class SPECIFIC_TAGS(Enum):
    IMPORTANT = Tag(
        "important",
        r_prefix=r"(?:\[\[\s*important\s*\]\]|\[\s*important\s*\]):?\s*",
    )

    HINT = Tag(
        "hint",
        r_prefix=r"(?:\[\[\s*hint\s*\]\]|\[\s*hint\s*\]):?\s*",
    )

    QUESTION = Tag(
        "question",
        r_prefix=r"(?:\[\[\s*(?:asked_question|question)\s*\]\]|\[\s*(?:asked_question|question)\s*\]):?\s*",
    )

    HIGHLIGHT = Tag(
        "highlight",
        r_prefix=r"(?:#{1,3})\s+",
    )

    LOAD_LINK = Tag(
        "load_link",
        r_prefix=r"\[\[\s*",
        r_content=UUID_PATTERN,
        r_postfix=r"\s*\]\]",
    )

    TAG = Tag(
        "tag",
        r_prefix=r"\[\[\s*",
        r_content=r"[^\]]+",
        r_postfix=r"\s*\]\]",
    )

    @classmethod
    def find_tag(cls, capture: str) -> TagMatch | None:
        for itm in cls:
            if mtch := itm.value.find_match(capture):
                return mtch


TAGS_RE = compile(r"(?P<prefix>\[\[?\s*tags\s*\]?\])(?P<content>.*)", IGNORECASE)
