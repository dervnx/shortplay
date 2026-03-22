from sqlalchemy import Column, BigInteger, String, Text, Integer, SmallInteger
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class Project(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Project model for short drama projects."""

    __tablename__ = "project"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    cover = Column(String(500), nullable=True)
    style_id = Column(BigInteger, nullable=True)
    status = Column(SmallInteger, default=0)  # 0-草稿 1-处理中 2-已完成
    consistency = Column(Integer, default=0)
    chapter_count = Column(Integer, default=0)
    progress = Column(Integer, default=0)

    # Relationships
    episodes = relationship("Episode", back_populates="project", cascade="all, delete-orphan")
    model_overrides = relationship("ProjectModelOverride", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name})>"
