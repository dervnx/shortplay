from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[ModelType]:
        """Get entity by ID."""
        return self.db.query(self.model).filter(
            self.model.id == id,
            self.model.is_deleted == 0
        ).first()

    def get_all(self) -> List[ModelType]:
        """Get all active entities."""
        return self.db.query(self.model).filter(
            self.model.is_deleted == 0
        ).all()

    def create(self, **kwargs) -> ModelType:
        """Create a new entity."""
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Update an entity."""
        instance = self.get(id)
        if instance:
            for key, value in kwargs.items():
                if value is not None and hasattr(instance, key):
                    setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        """Soft delete an entity."""
        instance = self.get(id)
        if instance:
            instance.is_deleted = 1
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """Count active entities."""
        return self.db.query(func.count(self.model.id)).filter(
            self.model.is_deleted == 0
        ).scalar()

    def paginate(self, page: int = 1, page_size: int = 10) -> tuple[List[ModelType], int]:
        """Paginate entities."""
        total = self.count()
        offset = (page - 1) * page_size
        items = self.db.query(self.model).filter(
            self.model.is_deleted == 0
        ).offset(offset).limit(page_size).all()
        return items, total
