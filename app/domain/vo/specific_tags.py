from re import compile, IGNORECASE
from enum import Enum, unique
from .tag import Tag

UUID_PATTERN = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"


@unique
class SPECIFIC_TAGS(Enum):
    IMPORTANT = Tag(
        "important",
        r_prefix=r"\[\[?\s*important\s*\]?\]:?\s*",
        r_postfix=r"(?:\s*\[\[?\s*important\s*\]?\])?",
    )
    HINT = Tag("hint", r_prefix=r"\[\[\s*hint\s*\]\]")
    QUESTION = Tag(
        "question", r_prefix=r"\[\[?\s*(?:asked_guestion|question)\s*\]?\]:?\s*"
    )
    HIGHLIGHT = Tag("hightlight", r_prefix=r"#{1,3}\s")
    LOAD_LINK = Tag(
        "load_link",
        r_prefix=r"\[\[\s*",
        r_content=UUID_PATTERN,
        r_postfix=r"\s*\]\]",
    )
    TAG = Tag("tag", r_prefix=r"\[\[?\s*", r_postfix=r"\s*\]?\]")


TAGS_RE = compile(r"(?P<prefix>\[\[?\s*tags\s*\]?\])(?P<content>.*)", IGNORECASE)
