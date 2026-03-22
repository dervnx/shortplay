from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base project schema."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    cover: Optional[str] = None
    style_id: Optional[int] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""

    status: Optional[int] = 0


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    cover: Optional[str] = None
    style_id: Optional[int] = None
    status: Optional[int] = None


class ProjectResponse(BaseModel):
    """Schema for project response."""

    id: int
    name: str
    description: Optional[str] = None
    cover: Optional[str] = None
    style_id: Optional[int] = None
    status: int = 0
    consistency: int = 0
    chapter_count: int = 0
    progress: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Schema for paginated project list."""

    items: List[ProjectResponse]
    total: int
    page: int
    page_size: int
