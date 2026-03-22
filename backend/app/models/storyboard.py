from sqlalchemy import Column, BigInteger, String, Text, Integer, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class Storyboard(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Storyboard model for shot sequences."""

    __tablename__ = "storyboard"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    episode_id = Column(BigInteger, ForeignKey("episode.id", ondelete="CASCADE"), nullable=False)
    shot_number = Column(Integer, nullable=False)
    shot_type = Column(SmallInteger, default=1)  # 1-远景 2-中景 3-近景 4-特写
    duration = Column(Integer, default=5)  # 秒
    description = Column(Text, nullable=False)
    dialogue = Column(Text, nullable=True)
    thumbnail = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    image_prompt = Column(Text, nullable=True)
    video_prompt = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)

    # Relationships
    episode = relationship("Episode", back_populates="storyboards")
    storyboard_characters = relationship("StoryboardCharacter", back_populates="storyboard", cascade="all, delete-orphan")
    storyboard_scenes = relationship("StoryboardScene", back_populates="storyboard", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Storyboard(id={self.id}, shot_number={self.shot_number})>"


class StoryboardCharacter(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Association table for storyboard-character many-to-many relationship."""

    __tablename__ = "storyboard_character"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    episode_id = Column(BigInteger, nullable=False)
    storyboard_id = Column(BigInteger, ForeignKey("storyboard.id", ondelete="CASCADE"), nullable=False)
    character_id = Column(BigInteger, ForeignKey("character.id", ondelete="CASCADE"), nullable=False)
    project_id = Column(BigInteger, nullable=False)

    # Relationships
    storyboard = relationship("Storyboard", back_populates="storyboard_characters")
    character = relationship("Character", back_populates="storyboard_characters")


class StoryboardScene(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Association table for storyboard-scene many-to-many relationship."""

    __tablename__ = "storyboard_scene"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    episode_id = Column(BigInteger, nullable=False)
    storyboard_id = Column(BigInteger, ForeignKey("storyboard.id", ondelete="CASCADE"), nullable=False)
    scene_id = Column(BigInteger, ForeignKey("scene.id", ondelete="CASCADE"), nullable=False)
    project_id = Column(BigInteger, nullable=False)

    # Relationships
    storyboard = relationship("Storyboard", back_populates="storyboard_scenes")
    scene = relationship("Scene", back_populates="storyboard_scenes")
