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
from app.schemas.episode import (
    EpisodeCreate,
    EpisodeUpdate,
    EpisodeResponse,
    EpisodeListResponse,
)
from app.schemas.character import (
    CharacterCreate,
    CharacterUpdate,
    CharacterResponse,
    CharacterListResponse,
)
from app.schemas.scene import (
    SceneCreate,
    SceneUpdate,
    SceneResponse,
    SceneListResponse,
)
from app.services.project_service import ProjectService
from app.services.episode_service import EpisodeService
from app.services.character_service import CharacterService
from app.services.scene_service import SceneService

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


@router.post("/{project_id}/episodes", response_model=BaseResponse[EpisodeResponse])
def create_episode(
    project_id: int,
    schema: EpisodeCreate,
    db: Session = Depends(get_db_session),
):
    """Create a new episode for a project."""
    # Verify project exists
    project_service = ProjectService(db)
    project = project_service.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    service = EpisodeService(db)
    episode = service.create(project_id, schema)
    return BaseResponse(data=EpisodeResponse.model_validate(episode))


@router.get("/{project_id}/episodes", response_model=BaseResponse[EpisodeListResponse])
def list_episodes(
    project_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_session),
):
    """List episodes for a project."""
    # Verify project exists
    project_service = ProjectService(db)
    project = project_service.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    service = EpisodeService(db)
    result = service.list_by_project(project_id, page, page_size)
    items = [EpisodeResponse.model_validate(e) for e in result.items]
    return BaseResponse(data=EpisodeListResponse(
        items=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    ))


@router.post("/{project_id}/characters", response_model=BaseResponse[CharacterResponse])
def create_character(
    project_id: int,
    schema: CharacterCreate,
    db: Session = Depends(get_db_session),
):
    """Create a new character for a project."""
    # Verify project exists
    project_service = ProjectService(db)
    project = project_service.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    service = CharacterService(db)
    character = service.create(project_id, schema)
    return BaseResponse(data=CharacterResponse.model_validate(character))


@router.get("/{project_id}/characters", response_model=BaseResponse[CharacterListResponse])
def list_characters(
    project_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db_session),
):
    """List characters for a project."""
    # Verify project exists
    project_service = ProjectService(db)
    project = project_service.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    service = CharacterService(db)
    result = service.list_by_project(project_id, keyword, page, page_size)
    items = [CharacterResponse.model_validate(c) for c in result.items]
    return BaseResponse(data=CharacterListResponse(
        items=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    ))


@router.post("/{project_id}/scenes", response_model=BaseResponse[SceneResponse])
def create_scene(
    project_id: int,
    schema: SceneCreate,
    db: Session = Depends(get_db_session),
):
    """Create a new scene for a project."""
    # Verify project exists
    project_service = ProjectService(db)
    project = project_service.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    service = SceneService(db)
    scene = service.create(project_id, schema)
    return BaseResponse(data=SceneResponse.model_validate(scene))


@router.get("/{project_id}/scenes", response_model=BaseResponse[SceneListResponse])
def list_scenes(
    project_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db_session),
):
    """List scenes for a project."""
    # Verify project exists
    project_service = ProjectService(db)
    project = project_service.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    service = SceneService(db)
    result = service.list_by_project(project_id, keyword, page, page_size)
    items = [SceneResponse.model_validate(s) for s in result.items]
    return BaseResponse(data=SceneListResponse(
        items=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    ))
