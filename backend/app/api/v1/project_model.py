from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_session
from app.schemas.common import BaseResponse
from app.schemas.project_model import (
    ProjectModelOverrideCreate,
    ProjectModelOverrideResponse,
    ProjectModelConfigResponse,
)
from app.repositories.project_model_override import ProjectModelOverrideRepository
from app.services.model_service import ModelService
from app.repositories.project import ProjectRepository

router = APIRouter()


@router.get("/projects/{project_id}/model-config", response_model=BaseResponse[ProjectModelConfigResponse])
def get_project_model_config(project_id: int, db: Session = Depends(get_db_session)):
    """Get project model configuration including overrides and global defaults."""
    # Verify project exists
    project_repo = ProjectRepository(db)
    project = project_repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get overrides
    override_repo = ProjectModelOverrideRepository(db)
    overrides = override_repo.get_by_project(project_id)
    override_map: Dict[int, int] = {o.model_type: o.model_instance_id for o in overrides}

    # Get defaults
    model_service = ModelService(db)
    defaults = model_service.get_defaults_by_type()

    return BaseResponse(data=ProjectModelConfigResponse(
        project_id=project_id,
        overrides=override_map,
        defaults={k: {"id": v.id, "instance_name": v.instance_name, "model_code": v.model_code} if v else None for k, v in defaults.items()}
    ))


@router.put("/projects/{project_id}/model-config", response_model=BaseResponse[ProjectModelOverrideResponse])
def set_project_model_override(
    project_id: int,
    schema: ProjectModelOverrideCreate,
    db: Session = Depends(get_db_session)
):
    """Set project model override for a specific type."""
    # Verify project exists
    project_repo = ProjectRepository(db)
    project = project_repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Verify instance exists
    model_service = ModelService(db)
    instance = model_service.get_instance(schema.model_instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Model instance not found")

    # Upsert override
    override_repo = ProjectModelOverrideRepository(db)
    override = override_repo.upsert(project_id, schema.model_instance_id, schema.model_type)

    return BaseResponse(data=ProjectModelOverrideResponse.model_validate(override))


@router.delete("/projects/{project_id}/model-config/{model_type}", response_model=BaseResponse[dict])
def delete_project_model_override(project_id: int, model_type: int, db: Session = Depends(get_db_session)):
    """Remove project model override for a specific type."""
    override_repo = ProjectModelOverrideRepository(db)
    override = override_repo.get_by_project_and_type(project_id, model_type)
    if not override:
        raise HTTPException(status_code=404, detail="Override not found")
    override_repo.delete(override.id)
    return BaseResponse(data={"project_id": project_id, "model_type": model_type, "deleted": True})