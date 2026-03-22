from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ProviderBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    provider_type: str = Field(..., min_length=1, max_length=50)  # openai/minimax/claude/custom
    api_base: Optional[str] = Field(None, max_length=255)
    api_key: Optional[str] = Field(None, max_length=500)
    status: int = Field(default=1, ge=0, le=1)


class ProviderCreate(ProviderBase):
    pass


class ProviderUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    provider_type: Optional[str] = Field(None, min_length=1, max_length=50)
    api_base: Optional[str] = Field(None, max_length=255)
    api_key: Optional[str] = Field(None, max_length=500)
    status: Optional[int] = Field(None, ge=0, le=1)


class ProviderResponse(ProviderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
