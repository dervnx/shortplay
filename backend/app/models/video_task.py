from sqlalchemy import Column, BigInteger, String, Text, Integer, SmallInteger, DateTime, ForeignKey

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class VideoTask(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Video task model for tracking video generation tasks."""

    __tablename__ = "video_task"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(BigInteger, nullable=False)
    instance_id = Column(BigInteger, nullable=False)  # 模型实例ID
    target_id = Column(BigInteger, nullable=False)  # 角色ID或分镜ID
    task_id = Column(String(50), default="")
    task_type = Column(SmallInteger, default=1)  # 1-角色视频 2-分镜视频 3-音视频合成
    status = Column(String(10), nullable=True)
    progress = Column(Integer, default=0)
    overall_progress = Column(Integer, default=0)
    video_url = Column(String(500), nullable=True)
    error_message = Column(Text, nullable=True)
    next_poll_at = Column(DateTime, nullable=True)
    poll_count = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<VideoTask(id={self.id}, status={self.status})>"
