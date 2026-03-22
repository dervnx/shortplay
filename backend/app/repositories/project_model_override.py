from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from app.models.project_model_override import ProjectModelOverride
from app.repositories.base import BaseRepository


class ProjectModelOverrideRepository(BaseRepository[ProjectModelOverride]):
    """Repository for project model override."""

    def __init__(self, db: Session):
        super().__init__(ProjectModelOverride, db)

    def get_by_project_and_type(self, project_id: int, model_type: int) -> Optional[ProjectModelOverride]:
        """Get override for specific project and model type."""
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.model_type == model_type,
            self.model.is_deleted == 0
        ).first()

    def get_by_project(self, project_id: int) -> List[ProjectModelOverride]:
        """Get all overrides for a project."""
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.is_deleted == 0
        ).all()

    def upsert(self, project_id: int, model_instance_id: int, model_type: int) -> ProjectModelOverride:
        """Create or update override for project and type."""
        existing = self.get_by_project_and_type(project_id, model_type)
        if existing:
            existing.model_instance_id = model_instance_id
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            return self.create(
                project_id=project_id,
                model_instance_id=model_instance_id,
                model_type=model_type
            )