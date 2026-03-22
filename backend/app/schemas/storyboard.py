from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class StoryboardBase(BaseModel):
    """Base storyboard schema."""

    shot_number: int = Field(..., ge=1)
    description: str
    shot_type: int = Field(default=1, ge=1, le=4)  # 1-远景 2-中景 3-近景 4-特写
    duration: int = Field(default=5, ge=1)
    dialogue: Optional[str] = None


class StoryboardCreate(StoryboardBase):
    """Schema for creating a storyboard."""

    episode_id: int


class StoryboardUpdate(BaseModel):
    """Schema for updating a storyboard."""

    description: Optional[str] = None
    shot_type: Optional[int] = Field(None, ge=1, le=4)
    duration: Optional[int] = Field(None, ge=1)
    dialogue: Optional[str] = None
    image_prompt: Optional[str] = None
    video_prompt: Optional[str] = None
    order_index: Optional[int] = None


class StoryboardGenerate(BaseModel):
    """Schema for generating storyboard."""

    model_instance_id: Optional[int] = None
    use_vector: bool = Field(default=False)


class StoryboardCharacterLink(BaseModel):
    """Schema for linking characters to storyboard."""

    character_ids: List[int] = Field(..., max_length=3)


class StoryboardSceneLink(BaseModel):
    """Schema for linking scene to storyboard."""

    scene_id: int


class CharacterBrief(BaseModel):
    """Brief character info for storyboard."""

    id: int
    name: str
    description: Optional[str] = None


class SceneBrief(BaseModel):
    """Brief scene info for storyboard."""

    id: int
    name: str
    description: Optional[str] = None


class StoryboardResponse(BaseModel):
    """Schema for storyboard response."""

    id: int
    episode_id: int
    shot_number: int
    shot_type: int
    duration: int
    description: str
    dialogue: Optional[str] = None
    thumbnail: Optional[str] = None
    video_url: Optional[str] = None
    image_prompt: Optional[str] = None
    video_prompt: Optional[str] = None
    order_index: int
    characters: List[CharacterBrief] = []
    scene: Optional[SceneBrief] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StoryboardListResponse(BaseModel):
    """Schema for paginated storyboard list."""

    items: List[StoryboardResponse]
    total: int
    page: int
    page_size: int
