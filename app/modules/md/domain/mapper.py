from .models import STARTING_TAG, TEXT_TAG, LINK_TAG, HORIZONTAL_TAG, Tag
from typing import Optional


def mapper_tag_name(prefix: str, postfix: Optional[str] = "") -> Tag:
    if isinstance(prefix, str) and isinstance(postfix, str):
        for _enum in (STARTING_TAG, TEXT_TAG, LINK_TAG, HORIZONTAL_TAG):
            for _tag in _enum:
                tag = _tag.value
                if tag == (prefix, postfix):
                    return _tag.value

    return Tag("text", "", "")
