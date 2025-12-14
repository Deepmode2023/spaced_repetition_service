from .models import Tag, Position
from typing import Optional
from .mapper import mapper_tag_name


class Token:
    position: Position
    content: str
    tag: Tag
    children: Optional[list["Token"]] = None

    def __init__(
        self,
        start: int,
        end: int,
        prefix: str,
        content: str,
        postfix: Optional[str] = "",
    ):
        self.position = Position(start, end)
        self.content = content
        self.tag = mapper_tag_name(prefix, postfix)

    def __str__(self):
        return f"Token(tag={self.tag.name}, position={self.position})"
