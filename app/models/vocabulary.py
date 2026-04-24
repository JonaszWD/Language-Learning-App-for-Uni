from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.utils.db import Base


class Vocabulary(Base):
    __tablename__ = "vocabularies"

    id         = Column(Integer, primary_key=True, index=True)
    word       = Column(String(255), nullable=False)
    translation= Column(String(255), nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    story_id   = Column(Integer, ForeignKey("posts.id"), nullable=False)
    anki_exported = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship back to the User model
    author = relationship("User", back_populates="vocabularies")
    story = relationship("Post", back_populates="vocabularies")

    def __repr__(self):
        return f"<Post id={self.id} word={self.word!r} translation={self.translation}>"