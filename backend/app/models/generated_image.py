from sqlalchemy import Column, BigInteger, String, Text, SmallInteger, ForeignKey

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class GeneratedImage(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Generated image model for storing AI generated images."""

    __tablename__ = "generated_image"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    episode_id = Column(BigInteger, ForeignKey("episode.id", ondelete="CASCADE"), nullable=False)
    image_type = Column(SmallInteger, default=1)  # 1-角色 2-场景
    target_id = Column(BigInteger, nullable=True)  # 关联角色或场景的ID
    image_url = Column(String(500), nullable=False)
    prompt = Column(Text, nullable=True)
    status = Column(SmallInteger, default=1)  # 0-生成中 1-成功 2-失败

    def __repr__(self):
        return f"<GeneratedImage(id={self.id}, type={self.image_type})>"
