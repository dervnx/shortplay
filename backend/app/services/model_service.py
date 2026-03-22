from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from app.models.model_definition import ModelDefinition
from app.models.model_instance import ModelInstance
from app.schemas.model import ModelDefinitionCreate, ModelInstanceCreate, ModelInstanceUpdate
from app.repositories.model_instance import ModelInstanceRepository, ModelInstanceDefaultRepository


class ModelService:
    """Service for model management business logic."""

    def __init__(self, db: Session):
        self.repo = ModelInstanceRepository(db)
        self.default_repo = ModelInstanceDefaultRepository(db)

    # Model Definition
    def create_definition(self, schema: ModelDefinitionCreate) -> ModelDefinition:
        """Create a new model definition."""
        from app.repositories.base import BaseRepository
        from app.models.model_definition import ModelDefinition

        class TempRepo(BaseRepository[ModelDefinition]):
            def __init__(self, db):
                super().__init__(ModelDefinition, db)

        repo = TempRepo(self.repo.db)
        return repo.create(
            provider_code=schema.provider_code,
            base_url=schema.base_url,
            status=schema.status,
        )

    def get_definition(self, id: int) -> Optional[ModelDefinition]:
        """Get model definition by ID."""
        from app.repositories.base import BaseRepository
        from app.models.model_definition import ModelDefinition

        class TempRepo(BaseRepository[ModelDefinition]):
            def __init__(self, db):
                super().__init__(ModelDefinition, db)

        repo = TempRepo(self.repo.db)
        return repo.get(id)

    def list_definitions(self) -> List[ModelDefinition]:
        """List all model definitions."""
        from app.repositories.base import BaseRepository
        from app.models.model_definition import ModelDefinition

        class TempRepo(BaseRepository[ModelDefinition]):
            def __init__(self, db):
                super().__init__(ModelDefinition, db)

        repo = TempRepo(self.repo.db)
        return repo.get_all()

    # Model Instance
    def create_instance(self, schema: ModelInstanceCreate) -> ModelInstance:
        """Create a new model instance."""
        return self.repo.create(
            model_def_id=getattr(schema, 'model_def_id', None),
            model_code=schema.model_code,
            model_type=schema.model_type,
            instance_name=schema.instance_name,
            provider_id=schema.provider_id,
            scene_code=schema.scene_code,
            api_key=schema.api_key,
            params=schema.params,
            path=schema.path,
            is_default=schema.is_default,
            status=1,
        )

    def get_instance(self, id: int) -> Optional[ModelInstance]:
        """Get model instance by ID."""
        return self.repo.get(id)

    def list_instances(
        self,
        model_type: Optional[int] = None,
        scene_code: Optional[int] = None,
        provider_id: Optional[int] = None,
    ) -> List[ModelInstance]:
        """List model instances with filters."""
        if model_type:
            return self.repo.get_by_type(model_type)
        if scene_code:
            return self.repo.get_by_scene(scene_code)
        if provider_id:
            return self.repo.get_by_provider(provider_id)
        return self.repo.get_all()

    def get_default_instance(self, model_type: int) -> Optional[ModelInstance]:
        """Get default model instance by type."""
        return self.repo.get_default_by_type(model_type)

    def get_defaults_by_type(self) -> Dict[int, ModelInstance]:
        """Return dict of {model_type: default_instance}."""
        instances = self.repo.get_all()
        defaults = {}
        for instance in instances:
            if instance.is_default:
                defaults[instance.model_type] = instance
        return defaults

    def set_default(self, instance_id: int, model_type: int) -> None:
        """Set instance as default for its type, unset other defaults for same type."""
        # First, unset all defaults for this model_type
        all_instances = self.repo.get_by_type(model_type)
        for instance in all_instances:
            if instance.is_default:
                self.repo.update(instance.id, is_default=False)
        # Then set the new default
        self.repo.update(instance_id, is_default=True)

    def update_instance(self, id: int, schema: ModelInstanceUpdate) -> Optional[ModelInstance]:
        """Update a model instance."""
        update_data = schema.model_dump(exclude_unset=True)
        return self.repo.update(id, **update_data)

    def delete_instance(self, id: int) -> bool:
        """Delete a model instance."""
        return self.repo.delete(id)

    def set_default_instance(self, model_type: int, instance_id: int):
        """Set default model instance for a type."""
        return self.default_repo.set_default(model_type, instance_id)
