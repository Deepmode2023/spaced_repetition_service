from .models import Tag, Position
from typing import Optional, Iterable
from .mapper import mapper_tag_name
from dataclasses import dataclass, field


@dataclass(slots=True, eq=False)
class FlatToken:
    start: int
    end: int
    tag: str
    children: list["FlatToken"] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "start": self.start,
            "end": self.end,
            "tag": self.tag,
            "children": [child.to_dict() for child in self.children],
        }


class Token:
    position: Position
    content: str
    tag: Tag
    parent: Optional["Token"] = None

    def __init__(
        self,
        start: int,
        end: int,
        content: str,
        prefix: str,
        postfix: Optional[str] = "",
    ):
        if not all(isinstance(field, int) and field >= 0 for field in (start, end)):
            raise ValueError(
                "Please enter the correct data type `positive int` for `start`, `end`"
            )
        if not isinstance(content, str):
            raise ValueError("Please enter the correct data type `str` for `content`")

        self.position = Position(start, end)
        self.content = content
        self.tag = mapper_tag_name(prefix, postfix)

        self.children: list["Token"] = []

    def __str__(self):
        return f"Token(tag={self.tag.name}, start={self.position.start}, end={self.position.end})"

    def set_child(self, token: "Token"):
        if not isinstance(token, Token):
            raise ValueError("The children must have the Token class!")

        if token is self:
            raise ValueError("Token cannot be a child of itself")

        if token.parent is None:
            token.parent = self

        self.children.append(token)

    def set_children(self, tokens: list["Token"] | tuple["Token"]) -> None:
        if not isinstance(tokens, (list, tuple)):
            raise ValueError("Type of `tokens` must to be `list` or `tuple`!")

        for token in tokens:
            self.set_child(token)

    def flat_token(self) -> FlatToken:
        return FlatToken(
            start=self.position.start,
            end=self.position.end,
            tag=self.tag.name,
            children=self._children_to_flat(self.children),
        )

    def _children_to_flat(self, children: list["Token"]) -> list[FlatToken]:
        result: list[FlatToken] = []

        for child in children:
            flat_child = FlatToken(
                start=child.position.start,
                end=child.position.end,
                tag=child.tag.name,
                children=self._children_to_flat(child.children),
            )
            result.append(flat_child)

        return result
