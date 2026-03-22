from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class ProjectModelOverrideBase(BaseModel):
    model_instance_id: int
    model_type: int = Field(..., ge=1, le=4)


class ProjectModelOverrideCreate(ProjectModelOverrideBase):
    pass


class ProjectModelOverrideResponse(ProjectModelOverrideBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectModelConfigResponse(BaseModel):
    """Project model config with overrides and defaults."""
    project_id: int
    overrides: Dict[int, Optional[int]]  # {model_type: instance_id or None}
    defaults: Dict[int, Optional[Dict]]  # {model_type: instance details or None}