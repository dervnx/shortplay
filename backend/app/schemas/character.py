from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class CharacterBase(BaseModel):
    """Base character schema."""

    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=500)


class CharacterCreate(CharacterBase):
    """Schema for creating a character."""

    episode_id: int


class CharacterUpdate(BaseModel):
    """Schema for updating a character."""

    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    avatar: Optional[str] = None
    features: Optional[dict] = None


class CharacterResponse(BaseModel):
    """Schema for character response."""

    id: int
    episode_id: int
    project_id: int
    name: str
    description: Optional[str] = None
    avatar: Optional[str] = None
    video_url: Optional[str] = None
    features: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CharacterListResponse(BaseModel):
    """Schema for paginated character list."""

    items: List[CharacterResponse]
    total: int
    page: int
    page_size: int
