from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_session
from app.schemas.common import BaseResponse
from app.schemas.episode import (
    EpisodeCreate,
    EpisodeUpdate,
    EpisodeResponse,
    EpisodeListResponse,
)
from app.services.episode_service import EpisodeService
from app.services.character_service import CharacterService
from app.services.scene_service import SceneService
from app.core.skills_runtime import FilmEntityExtractor

router = APIRouter()


@router.post("/projects/{project_id}/episodes", response_model=BaseResponse[EpisodeResponse])
def create_episode(
    project_id: int,
    schema: EpisodeCreate,
    db: Session = Depends(get_db_session),
):
    """Create a new episode for a project."""
    service = EpisodeService(db)
    episode = service.create(project_id, schema)
    return BaseResponse(data=EpisodeResponse.model_validate(episode))


@router.get("/projects/{project_id}/episodes", response_model=BaseResponse[EpisodeListResponse])
def list_episodes(
    project_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_session),
):
    """List episodes for a project."""
    service = EpisodeService(db)
    result = service.list_by_project(project_id, page, page_size)
    items = [EpisodeResponse.model_validate(e) for e in result.items]
    return BaseResponse(data=EpisodeListResponse(
        items=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    ))


@router.get("/{episode_id}", response_model=BaseResponse[EpisodeResponse])
def get_episode(
    episode_id: int,
    db: Session = Depends(get_db_session),
):
    """Get episode by ID."""
    service = EpisodeService(db)
    episode = service.get(episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return BaseResponse(data=EpisodeResponse.model_validate(episode))


@router.put("/{episode_id}", response_model=BaseResponse[EpisodeResponse])
def update_episode(
    episode_id: int,
    schema: EpisodeUpdate,
    db: Session = Depends(get_db_session),
):
    """Update an episode."""
    service = EpisodeService(db)
    episode = service.update(episode_id, schema)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return BaseResponse(data=EpisodeResponse.model_validate(episode))


@router.delete("/{episode_id}", response_model=BaseResponse[dict])
def delete_episode(
    episode_id: int,
    db: Session = Depends(get_db_session),
):
    """Delete an episode."""
    service = EpisodeService(db)
    success = service.delete(episode_id)
    if not success:
        raise HTTPException(status_code=404, detail="Episode not found")
    return BaseResponse(data={"id": episode_id, "deleted": True})


@router.post("/{episode_id}/extract", response_model=BaseResponse[dict])
async def extract_info(
    episode_id: int,
    model_instance_id: Optional[int] = None,
    use_vector: bool = False,
    db: Session = Depends(get_db_session),
):
    """Extract characters and scenes from episode content using LLM.

    This endpoint uses the FilmEntityExtractor skill to analyze the episode's
    script text and extract structured information about characters and scenes.
    """
    service = EpisodeService(db)
    episode = service.get(episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    if not episode.content:
        raise HTTPException(status_code=400, detail="Episode has no content to extract")

    # Initialize the entity extractor
    extractor = FilmEntityExtractor()

    # Extract entities from script
    result = await extractor.extract(episode.content)

    # Bulk create characters and scenes
    char_service = CharacterService(db)
    scene_service = SceneService(db)

    characters_data = result.get("characters", [])
    scenes_data = result.get("scenes", [])

    # Create characters
    created_chars = char_service.bulk_create(
        project_id=episode.project_id,
        episode_id=episode_id,
        characters=characters_data,
    )

    # Create scenes
    created_scenes = scene_service.bulk_create(
        project_id=episode.project_id,
        episode_id=episode_id,
        scenes=scenes_data,
    )

    # Update episode step
    service.update_step(episode_id, current_step=1)

    return BaseResponse(data={
        "characters": [{"id": c.id, "name": c.name, "description": getattr(c, "description", "")} for c in created_chars],
        "scenes": [{"id": s.id, "name": s.name, "description": getattr(s, "description", "")} for s in created_scenes],
        "message": f"Extraction completed. {len(created_chars)} characters, {len(created_scenes)} scenes.",
        "raw_result": result.get("raw_output", ""),
    })


@router.post("/{episode_id}/characters/bulk", response_model=BaseResponse[dict])
def bulk_create_characters(
    episode_id: int,
    characters: list[dict],
    db: Session = Depends(get_db_session),
):
    """Bulk create characters for an episode."""
    episode_service = EpisodeService(db)
    episode = episode_service.get(episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    char_service = CharacterService(db)
    created = char_service.bulk_create(episode.project_id, episode_id, characters)

    return BaseResponse(data={
        "characters": [{"id": c.id, "name": c.name} for c in created],
        "total": len(created),
    })


@router.post("/{episode_id}/scenes/bulk", response_model=BaseResponse[dict])
def bulk_create_scenes(
    episode_id: int,
    scenes: list[dict],
    db: Session = Depends(get_db_session),
):
    """Bulk create scenes for an episode."""
    episode_service = EpisodeService(db)
    episode = episode_service.get(episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    scene_service = SceneService(db)
    created = scene_service.bulk_create(episode.project_id, episode_id, scenes)

    return BaseResponse(data={
        "scenes": [{"id": s.id, "name": s.name} for s in created],
        "total": len(created),
    })
