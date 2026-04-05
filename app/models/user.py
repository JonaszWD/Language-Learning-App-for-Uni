from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

from app.utils.db import Base


class User(Base):
    __tablename__ = "users"

    id          = Column(Integer, primary_key=True)
    name        = Column(String(100),unique=True, nullable=False)
    password    = Column(LargeBinary, nullable=False)
    created_at  = Column(DateTime, default=datetime.now)

    # Relationship to the posts and stories model
    posts = relationship("Post", back_populates="author")
    vocabularies = relationship("Vocabulary", back_populates="author")


    def __repr__(self):
        return f"<User name={self.name}> id={self.id}"