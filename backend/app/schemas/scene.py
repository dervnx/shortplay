from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class SceneBase(BaseModel):
    """Base scene schema."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class SceneCreate(SceneBase):
    """Schema for creating a scene."""

    episode_id: int


class SceneUpdate(BaseModel):
    """Schema for updating a scene."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    thumbnail: Optional[str] = None


class SceneResponse(BaseModel):
    """Schema for scene response."""

    id: int
    episode_id: int
    project_id: int
    name: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SceneListResponse(BaseModel):
    """Schema for paginated scene list."""

    items: List[SceneResponse]
    total: int
    page: int
    page_size: int
