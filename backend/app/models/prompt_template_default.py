from sqlalchemy import Column, BigInteger, String, SmallInteger

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class PromptTemplateDefault(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Default prompt template configuration per scene."""

    __tablename__ = "prompt_template_default"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    prompt_template_id = Column(BigInteger, nullable=False)
    status = Column(SmallInteger, default=1)
    scene_code = Column(SmallInteger, nullable=False)
    remark = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<PromptTemplateDefault(scene={self.scene_code}, template={self.prompt_template_id})>"
