from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_session
from app.schemas.common import BaseResponse
from app.schemas.scene import (
    SceneCreate,
    SceneUpdate,
    SceneResponse,
    SceneListResponse,
)
from app.services.scene_service import SceneService

router = APIRouter()


@router.get("/projects/{project_id}/scenes", response_model=BaseResponse[SceneListResponse])
def list_scenes(
    project_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db_session),
):
    """List scenes for a project."""
    service = SceneService(db)
    result = service.list_by_project(project_id, keyword, page, page_size)
    items = [SceneResponse.model_validate(s) for s in result.items]
    return BaseResponse(data=SceneListResponse(
        items=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    ))


@router.post("/projects/{project_id}/scenes", response_model=BaseResponse[SceneResponse])
def create_scene(
    project_id: int,
    schema: SceneCreate,
    db: Session = Depends(get_db_session),
):
    """Create a new scene."""
    service = SceneService(db)
    scene = service.create(project_id, schema)
    return BaseResponse(data=SceneResponse.model_validate(scene))


@router.get("/{scene_id}", response_model=BaseResponse[SceneResponse])
def get_scene(
    scene_id: int,
    db: Session = Depends(get_db_session),
):
    """Get scene by ID."""
    service = SceneService(db)
    scene = service.get(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    return BaseResponse(data=SceneResponse.model_validate(scene))


@router.put("/{scene_id}", response_model=BaseResponse[SceneResponse])
def update_scene(
    scene_id: int,
    schema: SceneUpdate,
    db: Session = Depends(get_db_session),
):
    """Update a scene."""
    service = SceneService(db)
    scene = service.update(scene_id, schema)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    return BaseResponse(data=SceneResponse.model_validate(scene))


@router.delete("/{scene_id}", response_model=BaseResponse[dict])
def delete_scene(
    scene_id: int,
    db: Session = Depends(get_db_session),
):
    """Delete a scene."""
    service = SceneService(db)
    success = service.delete(scene_id)
    if not success:
        raise HTTPException(status_code=404, detail="Scene not found")
    return BaseResponse(data={"id": scene_id, "deleted": True})


@router.post("/{scene_id}/thumbnail", response_model=BaseResponse[SceneResponse])
def update_scene_thumbnail(
    scene_id: int,
    thumbnail: str,
    db: Session = Depends(get_db_session),
):
    """Update scene thumbnail URL."""
    service = SceneService(db)
    scene = service.update_thumbnail(scene_id, thumbnail)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    return BaseResponse(data=SceneResponse.model_validate(scene))
