from uuid import uuid4

import sqlalchemy as db
from sqlalchemy.orm import relationship

from app.infrastucture.db.base import Base


class Tag(Base):
    __tablename__ = "tags"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    start_pos = db.Column(db.Integer, nullable=False)
    end_pos = db.Column(db.Integer, nullable=False)
    md_id = db.Column(db.String(36), db.ForeignKey("mds.id"))
    space_count = db.Column(db.Integer, default=0)
    md = relationship("MD", back_populates="tags")
    content = db.Column(db.String, nullable=False)
    type = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": "tag",
        "polymorphic_on": "type",
    }

    def __repr__(self):
        return (
            f"Tag(id={self.id} md_id start_pos={self.start_pos} end_pos={self.end_pos})"
        )

    @property
    def to_json(self):
        return {
            "id": self.id,
            "start_pos": self.start_pos,
            "end_pos": self.end_pos,
            "md_id": self.md_id,
            "content": self.content,
            "type": self.type,
        }
