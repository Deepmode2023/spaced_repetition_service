from .entities import Tag
from enum import Enum


class HORIZONTAL_TAG(Enum):
    OPTION_ONE = Tag("hr", "***", "")
    OPTION_SECOND = Tag("hr", "___", "")

    def __iter__(self):
        for value in self.__class__.__dict__.values():
            if isinstance(value, Tag):
                yield value


class LINK_TAG(Enum):
    LINK = Tag("link", "[", ")")
    UNIQ_LINK = Tag("uniq_link", "[[", "]]")
    NOTE_TAG = Tag("note_tag", "[[_nt", "nt_]]")

    def __iter__(self):
        for value in self.__class__.__dict__.values():
            if isinstance(value, Tag):
                yield value


class TEXT_TAG(Enum):
    BACKQUOTE = Tag("backquote", "`", "`")
    ITALIC = Tag("italic", "*", "*")
    BOLD = Tag("bold", "**", "**")
    STRIKETHROUGH = Tag("strikethrough", "~~", "~~")
    HIGHLIGHT = Tag("highlight", "==", "==")
    INLINE_CODE = Tag("inline_code", "`", "`")
    IMAGE = Tag("image", "! [", ")")
    FOOTNOTE = Tag("footnote", "^ [", "]")
    TAG = Tag("hash_tag", "#", "")
    MATH_INLINE = Tag("math_inline", "$", "$")

    def __iter__(self):
        for value in self.__class__.__dict__.values():
            if isinstance(value, Tag):
                yield value


class STARTING_TAG(Enum):
    H1 = Tag("h1", "# ", "")
    H2 = Tag("h2", "## ", "")
    H3 = Tag("h3", "### ", "")
    H4 = Tag("h4", "#### ", "")
    H5 = Tag("h5", "##### ", "")
    H6 = Tag("h6", "###### ", "")

    BLOCKQUOTE = Tag("blockquote", "> ", "")
    CODEBLOCK = Tag("codeblock", "```", "```")
    UL_LIST = Tag("list_ul", "- ", "")
    OL_LIST = Tag("list_ol", "1. ", "")
    TASK = Tag("task", "- [ ] ", "")
    TASK_DONE = Tag("task_done", "- [x] ", "")

    TABLE = Tag("table", "|", "|")
    HR = Tag("hr", "---", "")

    MATH_BLOCK = Tag("math_block", "$$", "$$")
    CALLOUT = Tag("callout", "> [!", "]")
    YAML_FRONT = Tag("yaml_frontmatter", "---", "---")

    def __iter__(self):
        for value in self.__class__.__dict__.values():
            if isinstance(value, Tag):
                yield value
