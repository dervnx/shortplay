from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class PromptTemplateBase(BaseModel):
    """Base prompt template schema."""

    prompt_code: str = Field(..., min_length=1, max_length=64)
    prompt_name: str = Field(..., min_length=1, max_length=128)
    scene_code: int = Field(..., ge=1)
    prompt_content: str = Field(..., min_length=1)


class PromptTemplateCreate(PromptTemplateBase):
    """Schema for creating a prompt template."""

    pass


class PromptTemplateUpdate(BaseModel):
    """Schema for updating a prompt template."""

    prompt_name: Optional[str] = Field(None, min_length=1, max_length=128)
    prompt_content: Optional[str] = Field(None, min_length=1)


class PromptTemplateResponse(BaseModel):
    """Schema for prompt template response."""

    id: int
    prompt_code: str
    prompt_name: str
    scene_code: int
    prompt_content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PromptTemplateListResponse(BaseModel):
    """Schema for paginated prompt template list."""

    items: List[PromptTemplateResponse]
    total: int
    page: int
    page_size: int
