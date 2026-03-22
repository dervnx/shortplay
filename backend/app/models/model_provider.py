from sqlalchemy import Column, BigInteger, String, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class ModelProvider(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Model provider configuration (OpenAI, MiniMax, Claude, custom)."""

    __tablename__ = "model_provider"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    provider_type = Column(String(50), nullable=False)  # openai/minimax/claude/custom
    api_base = Column(String(255), nullable=True)
    api_key = Column(String(500), nullable=True)
    status = Column(SmallInteger, default=1)  # 0=disabled, 1=enabled

    # Relationships
    instances = relationship("ModelInstance", back_populates="provider")
