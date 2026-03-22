from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.model_instance import ModelInstance
from app.models.model_instance_default import ModelInstanceDefault
from app.repositories.base import BaseRepository


class ModelInstanceRepository(BaseRepository[ModelInstance]):
    """Repository for ModelInstance model."""

    def __init__(self, db: Session):
        super().__init__(ModelInstance, db)

    def get_by_type(self, model_type: int) -> List[ModelInstance]:
        """Get all model instances by type."""
        return self.db.query(ModelInstance).filter(
            ModelInstance.model_type == model_type,
            ModelInstance.status == 1,
            ModelInstance.is_deleted == 0
        ).all()

    def get_by_scene(self, scene_code: int) -> List[ModelInstance]:
        """Get all model instances by scene."""
        return self.db.query(ModelInstance).filter(
            ModelInstance.scene_code == scene_code,
            ModelInstance.status == 1,
            ModelInstance.is_deleted == 0
        ).all()

    def get_default_by_type(self, model_type: int) -> Optional[ModelInstance]:
        """Get default model instance by type."""
        default = self.db.query(ModelInstanceDefault).filter(
            ModelInstanceDefault.model_type == model_type,
            ModelInstanceDefault.status == 1,
            ModelInstanceDefault.is_deleted == 0
        ).first()

        if default:
            return self.get(default.model_instance_id)
        return None


class ModelInstanceDefaultRepository:
    """Repository for ModelInstanceDefault model."""

    def __init__(self, db: Session):
        self.db = db

    def set_default(self, model_type: int, model_instance_id: int) -> ModelInstanceDefault:
        """Set default model instance for a type."""
        # Remove existing default
        self.db.query(ModelInstanceDefault).filter(
            ModelInstanceDefault.model_type == model_type,
            ModelInstanceDefault.is_deleted == 0
        ).update({"is_deleted": 1})

        # Create new default
        default = ModelInstanceDefault(
            model_type=model_type,
            model_instance_id=model_instance_id,
            status=1,
        )
        self.db.add(default)
        self.db.commit()
        self.db.refresh(default)
        return default

    def get_default(self, model_type: int) -> Optional[ModelInstanceDefault]:
        """Get default model instance for a type."""
        return self.db.query(ModelInstanceDefault).filter(
            ModelInstanceDefault.model_type == model_type,
            ModelInstanceDefault.status == 1,
            ModelInstanceDefault.is_deleted == 0
        ).first()
