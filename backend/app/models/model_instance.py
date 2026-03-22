from sqlalchemy import Column, BigInteger, String, SmallInteger, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin

class ModelInstance(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Model instance for specific model configurations."""

    __tablename__ = "model_instance"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    # New: link to provider
    provider_id = Column(BigInteger, ForeignKey("model_provider.id"), nullable=True)
    # Keep for backward compat
    model_def_id = Column(BigInteger, ForeignKey("model_definition.id"), nullable=True)
    model_code = Column(String(100), nullable=False)  # gpt-4o / qwen-max / MiniMax-Text-01
    model_type = Column(SmallInteger, nullable=False, default=1)  # 1-TEXT 2-IMAGE 3-VIDEO 4-AUDIO
    instance_name = Column(String(100), nullable=False)
    scene_code = Column(SmallInteger, nullable=True)  # nullable for new structure
    path = Column(String(50), nullable=True)
    api_key = Column(String(500), nullable=True)  # increased size, nullable
    params = Column(JSONB, nullable=True)  # temperature, max_tokens, etc.
    is_default = Column(Boolean, default=False, nullable=False)  # NEW: global default for type
    status = Column(SmallInteger, default=1)

    # Relationships
    provider = relationship("ModelProvider", back_populates="instances", foreign_keys=[provider_id])
    definition = relationship("ModelDefinition", back_populates="instances")

    def __repr__(self):
        return f"<ModelInstance(id={self.id}, name={self.instance_name})>"
