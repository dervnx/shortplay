from sqlalchemy import Column, BigInteger, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class Character(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Character model for roles in the story."""

    __tablename__ = "character"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    episode_id = Column(BigInteger, ForeignKey("episode.id", ondelete="CASCADE"), nullable=False)
    project_id = Column(BigInteger, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    avatar = Column(String(1024), nullable=True)
    video_url = Column(String(500), nullable=True)
    features = Column(JSONB, nullable=True)  # 角色特征描述

    # Relationships
    episode = relationship("Episode", back_populates="characters")
    storyboard_characters = relationship("StoryboardCharacter", back_populates="character")

    def __repr__(self):
        return f"<Character(id={self.id}, name={self.name})>"
