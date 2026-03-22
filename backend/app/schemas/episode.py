from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class EpisodeBase(BaseModel):
    """Base episode schema."""

    name: str = Field(..., min_length=1, max_length=100)
    content: Optional[str] = None


class EpisodeCreate(EpisodeBase):
    """Schema for creating an episode."""

    chapter_number: int = Field(..., ge=1)


class EpisodeUpdate(BaseModel):
    """Schema for updating an episode."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = None
    status: Optional[int] = None
    current_step: Optional[int] = None


class EpisodeResponse(BaseModel):
    """Schema for episode response."""

    id: int
    project_id: int
    chapter_number: int
    name: str
    content: Optional[str] = None
    status: int = 0
    progress: int = 0
    current_step: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EpisodeListResponse(BaseModel):
    """Schema for paginated episode list."""

    items: List[EpisodeResponse]
    total: int
    page: int
    page_size: int


class ExtractionCharacter(BaseModel):
    """Schema for extracted character."""

    id: int
    name: str
    description: Optional[str] = None
    is_new: bool = True


class ExtractionScene(BaseModel):
    """Schema for extracted scene."""

    id: int
    name: str
    description: Optional[str] = None
    is_new: bool = True


class ExtractionResponse(BaseModel):
    """Schema for extraction result."""

    characters: List[ExtractionCharacter]
    scenes: List[ExtractionScene]
