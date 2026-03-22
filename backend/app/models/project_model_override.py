from sqlalchemy import Column, BigInteger, SmallInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin


class ProjectModelOverride(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Project-level model configuration override.

    Allows projects to override the global default model for specific model types.
    """

    __tablename__ = "project_model_override"
    __table_args__ = (
        UniqueConstraint('project_id', 'model_type', name='uq_project_model_type'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(BigInteger, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    model_instance_id = Column(BigInteger, ForeignKey("model_instance.id", ondelete="CASCADE"), nullable=False)
    model_type = Column(SmallInteger, nullable=False)  # 1-TEXT 2-IMAGE 3-VIDEO 4-AUDIO

    # Relationships
    project = relationship("Project", back_populates="model_overrides")

    def __repr__(self):
        return f"<ProjectModelOverride(project_id={self.project_id}, type={self.model_type})>"
