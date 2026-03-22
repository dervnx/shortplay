from sqlalchemy import Column, BigInteger, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class Scene(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Scene model for locations in the story."""

    __tablename__ = "scene"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    episode_id = Column(BigInteger, ForeignKey("episode.id", ondelete="CASCADE"), nullable=False)
    project_id = Column(BigInteger, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    thumbnail = Column(String(500), nullable=True)

    # Relationships
    episode = relationship("Episode", back_populates="scenes")
    storyboard_scenes = relationship("StoryboardScene", back_populates="scene")

    def __repr__(self):
        return f"<Scene(id={self.id}, name={self.name})>"
