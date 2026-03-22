from sqlalchemy import Column, BigInteger, String, SmallInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class ModelInstance(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Model instance for specific model configurations."""

    __tablename__ = "model_instance"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    model_def_id = Column(BigInteger, ForeignKey("model_definition.id"), nullable=False)
    model_code = Column(String(100), nullable=False)  # gpt-4o / qwen-max
    model_type = Column(SmallInteger, nullable=False, default=1)  # 1-TEXT 2-IMAGE 3-VIDEO 4-AUDIO
    instance_name = Column(String(100), nullable=False)
    scene_code = Column(SmallInteger, nullable=False)  # 1-通用文本 2-信息提取 3-角色生成...
    path = Column(String(50), nullable=True)
    api_key = Column(String(255), nullable=False)
    params = Column(JSONB, nullable=True)
    status = Column(SmallInteger, default=1)

    # Relationships
    definition = relationship("ModelDefinition", back_populates="instances")

    def __repr__(self):
        return f"<ModelInstance(id={self.id}, name={self.instance_name})>"
