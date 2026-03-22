from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_session
from app.schemas.common import BaseResponse
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
)
from app.services.project_service import ProjectService

router = APIRouter()


@router.post("", response_model=BaseResponse[ProjectResponse])
def create_project(
    schema: ProjectCreate,
    db: Session = Depends(get_db_session),
):
    """Create a new project."""
    service = ProjectService(db)
    project = service.create(schema)
    return BaseResponse(data=ProjectResponse.model_validate(project))


@router.get("", response_model=BaseResponse[ProjectListResponse])
def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[int] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db_session),
):
    """List projects with pagination and filters."""
    service = ProjectService(db)
    result = service.list(
        keyword=keyword,
        status=status,
        page=page,
        page_size=page_size,
    )
    items = [ProjectResponse.model_validate(p) for p in result.items]
    return BaseResponse(data=ProjectListResponse(
        items=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    ))


@router.get("/{project_id}", response_model=BaseResponse[ProjectResponse])
def get_project(
    project_id: int,
    db: Session = Depends(get_db_session),
):
    """Get project by ID."""
    service = ProjectService(db)
    project = service.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return BaseResponse(data=ProjectResponse.model_validate(project))


@router.put("/{project_id}", response_model=BaseResponse[ProjectResponse])
def update_project(
    project_id: int,
    schema: ProjectUpdate,
    db: Session = Depends(get_db_session),
):
    """Update a project."""
    service = ProjectService(db)
    project = service.update(project_id, schema)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return BaseResponse(data=ProjectResponse.model_validate(project))


@router.delete("/{project_id}", response_model=BaseResponse[dict])
def delete_project(
    project_id: int,
    db: Session = Depends(get_db_session),
):
    """Delete a project."""
    service = ProjectService(db)
    success = service.delete(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return BaseResponse(data={"id": project_id, "deleted": True})
