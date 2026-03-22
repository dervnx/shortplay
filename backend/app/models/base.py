from sqlalchemy import Column, Integer, SmallInteger, DateTime, func

# Import Base from app.core.database to ensure all models use the same declarative base
from app.core.database import Base

BaseModel = Base


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""

    is_deleted = Column(SmallInteger, default=0, nullable=False)

    @property
    def is_active(self) -> bool:
        return self.is_deleted == 0
