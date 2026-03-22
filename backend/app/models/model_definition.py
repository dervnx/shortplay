from sqlalchemy import Column, BigInteger, String, SmallInteger
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class ModelDefinition(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Model definition for AI providers (OpenAI, Aliyun, etc.)."""

    __tablename__ = "model_definition"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    provider_code = Column(String(50), nullable=False)  # openai / aliyun / baidu / volcengine
    base_url = Column(String(255), nullable=True)
    status = Column(SmallInteger, default=1)  # 1启用 0禁用

    # Relationships
    instances = relationship("ModelInstance", back_populates="definition")

    def __repr__(self):
        return f"<ModelDefinition(id={self.id}, provider={self.provider_code})>"
