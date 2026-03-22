from sqlalchemy import Column, BigInteger, String, SmallInteger
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class StyleTemplate(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Style template for image generation."""

    __tablename__ = "style_template"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)
    preview = Column(String(500), nullable=True)
    parameters = Column(JSONB, nullable=True)
    is_default = Column(SmallInteger, default=0)

    def __repr__(self):
        return f"<StyleTemplate(id={self.id}, name={self.name})>"
