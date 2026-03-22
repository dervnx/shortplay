from sqlalchemy import Column, BigInteger, String, SmallInteger

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class ModelInstanceDefault(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Default model instance configuration per model type."""

    __tablename__ = "model_instance_default"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    model_type = Column(SmallInteger, nullable=False)  # 1-TEXT 2-IMAGE 3-VIDEO 4-AUDIO
    model_instance_id = Column(BigInteger, nullable=False)
    status = Column(SmallInteger, default=1)
    remark = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<ModelInstanceDefault(type={self.model_type}, instance_id={self.model_instance_id})>"
