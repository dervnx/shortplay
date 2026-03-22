from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ModelDefinitionBase(BaseModel):
    """Base model definition schema."""

    provider_code: str = Field(..., min_length=1, max_length=50)
    base_url: Optional[str] = None
    status: int = Field(default=1, ge=0, le=1)


class ModelDefinitionCreate(ModelDefinitionBase):
    """Schema for creating a model definition."""

    pass


class ModelDefinitionResponse(BaseModel):
    """Schema for model definition response."""

    id: int
    provider_code: str
    base_url: Optional[str] = None
    status: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ModelInstanceBase(BaseModel):
    """Base model instance schema."""

    model_code: str = Field(..., min_length=1, max_length=100)  # gpt-4o / MiniMax-Text-01
    model_type: int = Field(..., ge=1, le=4)  # 1-TEXT 2-IMAGE 3-VIDEO 4-AUDIO
    instance_name: str = Field(..., min_length=1, max_length=100)
    provider_id: Optional[int] = None  # FK to model_provider
    scene_code: Optional[int] = None  # nullable for new structure
    api_key: Optional[str] = Field(None, max_length=500)
    params: Optional[dict] = None  # temperature, max_tokens, etc.
    path: Optional[str] = None
    is_default: bool = Field(default=False)


class ModelInstanceCreate(ModelInstanceBase):
    """Schema for creating a model instance."""
    pass


class ModelInstanceUpdate(BaseModel):
    """Schema for updating a model instance."""

    model_code: Optional[str] = Field(None, min_length=1, max_length=100)
    model_type: Optional[int] = Field(None, ge=1, le=4)
    instance_name: Optional[str] = Field(None, min_length=1, max_length=100)
    provider_id: Optional[int] = None
    scene_code: Optional[int] = None
    api_key: Optional[str] = Field(None, max_length=500)
    params: Optional[dict] = None
    path: Optional[str] = None
    is_default: Optional[bool] = None
    status: Optional[int] = None


class ModelInstanceResponse(BaseModel):
    """Schema for model instance response."""

    id: int
    model_def_id: Optional[int] = None
    provider_id: Optional[int] = None
    model_code: str
    model_type: int
    instance_name: str
    scene_code: Optional[int] = None
    path: Optional[str] = None
    params: Optional[dict] = None
    is_default: bool
    status: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ModelInstanceListResponse(BaseModel):
    """Schema for paginated model instance list."""

    items: List[ModelInstanceResponse]
    total: int
    page: int
    page_size: int
