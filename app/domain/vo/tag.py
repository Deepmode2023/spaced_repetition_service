from dataclasses import dataclass
from typing import Optional
from re import IGNORECASE, compile, Match
from typing import Union


@dataclass
class Tag:
    name: str
    r_prefix: str
    r_content: str
    r_postfix: str | None = None

    def __init__(
        self,
        name: str,
        r_prefix: str,
        r_content: Optional[str] = ".*",
        r_postfix: str | None = None,
    ):
        self.name = name
        self.r_prefix = r_prefix
        self.r_postfix = r_postfix
        self.r_content = r_content

        self._compiled_pattern = self._compile()

    def __repr__(self):
        return f"Tag(tag='{self.name}', pattern='{self.pattern}')"

    def __eq__(self, other):
        if not isinstance(other, Tag):
            return NotImplemented
        return (
            self.name == other.name
            and self.r_prefix == other.r_prefix
            and self.r_content == other.r_content
            and self.r_postfix == other.r_postfix
        )

    def _compile(self):
        return compile(self.pattern, IGNORECASE)

    def find_match(self, capture: str) -> Union["TagMatch", None]:
        if mtch := self._compiled_pattern.search(capture):
            return TagMatch.from_regex(mtch, self)

    @property
    def pattern(self) -> str:
        reg = rf"(?P<prefix>{self.r_prefix})(?P<content>{self.r_content})"
        if self.r_postfix:
            reg += rf"(?P<postfix>{self.r_postfix})"

        return reg


@dataclass(frozen=True)
class TagMatch:
    content: str
    prefix: str
    postfix: str | None
    tag: "Tag"

    @classmethod
    def from_regex(cls, match: Match, tag: "Tag") -> "TagMatch":
        if not isinstance(match, Match):
            raise TypeError("match must be re.Match")

        if not isinstance(tag, Tag):
            raise TypeError("tag must be Tag")

        return cls(
            content=match.group("content"),
            prefix=match.group("prefix"),
            postfix=match.groupdict().get("postfix"),
            tag=tag,
        )
