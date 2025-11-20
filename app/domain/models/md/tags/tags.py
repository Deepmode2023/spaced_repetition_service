from enum import Enum

import sqlalchemy as db

from .base import Tag


class TextStyleEnum(str, Enum):
    """Enumeration for different text styles in Markdown."""

    SIMPLE = "simple"
    ITALIC = "italic"
    BOLD = "bold"
    UNDERLINE = "underline"
    STRIKETHROUGH = "strikethrough"

    @classmethod
    def fields(cls):
        """
        Returns all fields of the enum as a dictionary.

        Returns:
            dict: A dictionary with enum names as keys and values as enum values.
        """
        return {item.name: item.value for item in cls}


class Text(Tag):
    """Represents formatted text in Markdown (e.g., bold, italic, underline)."""

    __tablename__ = "text"
    id = db.Column(
        db.String(36),
        db.ForeignKey("tags.id"),
        primary_key=True,
    )
    style = db.Column(db.String(20), nullable=False, default=TextStyleEnum.SIMPLE)

    __mapper_args__ = {"polymorphic_identity": "text"}

    def __repr__(self):
        return f"Text(id={self.id}, style={self.style})"

    def to_json(self):
        data = super().to_json()
        data.update({"style": self.style})
        return data


class Quote(Tag):
    """Represents block quotes in Markdown (e.g., '> This is a quote')."""

    __tablename__ = "quote"
    id = db.Column(
        db.String(36),
        db.ForeignKey("tags.id"),
        primary_key=True,
    )
    sup_quote = db.Column(db.Boolean, default=False)

    __mapper_args__ = {"polymorphic_identity": "quote"}

    def __repr__(self):
        return f"Quote(id={self.id}, sup_quote={self.sup_quote})"

    def to_json(self):
        data = super().to_json()
        data.update({"sup_quote": self.sup_quote})
        return data


class Heading(Tag):
    """Represents different levels of headings in Markdown (e.g., '# H1', '## H2')."""

    __tablename__ = "heading"
    id = db.Column(
        db.String(36),
        db.ForeignKey("tags.id"),
        primary_key=True,
    )
    level = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "heading"}

    def __repr__(self):
        return f"Heading(id={self.id}, level={self.level})"

    def to_json(self):
        data = super().to_json()
        data.update({"level": self.level})
        return data


class List(Tag):
    """Represents ordered (1. 2. 3.) and unordered (- * +) lists in Markdown."""

    __tablename__ = "list"
    id = db.Column(
        db.String(36),
        db.ForeignKey("tags.id"),
        primary_key=True,
    )
    ordered = db.Column(db.Boolean, default=False)

    __mapper_args__ = {"polymorphic_identity": "list"}

    def __repr__(self):
        return f"List(id={self.id}, ordered={self.ordered})"

    def to_json(self):
        data = super().to_json()
        data.update({"ordered": self.ordered})
        return data


class Code(Tag):
    """Represents code blocks in Markdown (e.g., triple-backtick code blocks)."""

    __tablename__ = "code"
    id = db.Column(
        db.String(36),
        db.ForeignKey("tags.id"),
        primary_key=True,
    )
    is_multiply = db.Column(db.Boolean, nullable=False, default=True)

    __mapper_args__ = {"polymorphic_identity": "code"}

    def __repr__(self):
        return f"Code(id={self.id}, is_multiply={self.is_multiply})"
