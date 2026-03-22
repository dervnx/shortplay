from sqlalchemy import Column, BigInteger, String, Text, Integer, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class Episode(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Episode model for chapters within a project."""

    __tablename__ = "episode"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(BigInteger, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    content = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)  # 0-待开始 1-处理中 2-已完成
    progress = Column(Integer, default=0)
    current_step = Column(SmallInteger, default=0)
    # current_step: 0-输入内容 1-提取信息 2-生成图片 4-固定角色 5-生成分镜 6-生成视频 7-合成完成

    # Relationships
    project = relationship("Project", back_populates="episodes")
    characters = relationship("Character", back_populates="episode", cascade="all, delete-orphan")
    scenes = relationship("Scene", back_populates="episode", cascade="all, delete-orphan")
    storyboards = relationship("Storyboard", back_populates="episode", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Episode(id={self.id}, name={self.name})>"
