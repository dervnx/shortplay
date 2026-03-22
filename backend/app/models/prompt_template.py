from sqlalchemy import Column, BigInteger, String, Text, SmallInteger

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class PromptTemplate(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Prompt template for various AI generation tasks."""

    __tablename__ = "prompt_template"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    prompt_code = Column(String(64), nullable=False, unique=True)
    prompt_name = Column(String(128), nullable=False)
    scene_code = Column(SmallInteger, nullable=False)  # SceneCode enum
    prompt_content = Column(Text, nullable=False)

    def __repr__(self):
        return f"<PromptTemplate(id={self.id}, code={self.prompt_code})>"
