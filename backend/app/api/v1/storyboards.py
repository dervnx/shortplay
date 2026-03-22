from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_session
from app.schemas.common import BaseResponse
from app.schemas.storyboard import (
    StoryboardCreate,
    StoryboardUpdate,
    StoryboardResponse,
    StoryboardListResponse,
    StoryboardCharacterLink,
    StoryboardSceneLink,
)
from app.services.storyboard_service import StoryboardService
from app.services.episode_service import EpisodeService

router = APIRouter()


def _storyboard_to_response(sb: dict) -> StoryboardResponse:
    """Convert storyboard dict to response model."""
    from app.schemas.storyboard import CharacterBrief, SceneBrief
    characters = [CharacterBrief(**c) for c in sb.get("characters", [])]
    scene = SceneBrief(**sb["scene"]) if sb.get("scene") else None
    return StoryboardResponse(
        id=sb["id"],
        episode_id=sb["episode_id"],
        shot_number=sb["shot_number"],
        shot_type=sb["shot_type"],
        duration=sb["duration"],
        description=sb["description"],
        dialogue=sb.get("dialogue"),
        thumbnail=sb.get("thumbnail"),
        video_url=sb.get("video_url"),
        image_prompt=sb.get("image_prompt"),
        video_prompt=sb.get("video_prompt"),
        order_index=sb.get("order_index", 0),
        characters=characters,
        scene=scene,
        created_at=sb["created_at"],
        updated_at=sb["updated_at"],
    )


@router.get("/episodes/{episode_id}/storyboards", response_model=BaseResponse[StoryboardListResponse])
def list_storyboards(
    episode_id: int,
    db: Session = Depends(get_db_session),
):
    """List storyboards for an episode."""
    service = StoryboardService(db)
    storyboards = service.list_by_episode(episode_id)
    items = [_storyboard_to_response(sb) for sb in storyboards]
    return BaseResponse(data=StoryboardListResponse(
        items=items,
        total=len(items),
        page=1,
        page_size=len(items),
    ))


@router.post("/episodes/{episode_id}/storyboards", response_model=BaseResponse[StoryboardResponse])
def create_storyboard(
    episode_id: int,
    schema: StoryboardCreate,
    db: Session = Depends(get_db_session),
):
    """Create a new storyboard."""
    service = StoryboardService(db)
    storyboard = service.create(episode_id, schema)
    return BaseResponse(data=_storyboard_to_response(storyboard))


@router.get("/{storyboard_id}", response_model=BaseResponse[StoryboardResponse])
def get_storyboard(
    storyboard_id: int,
    db: Session = Depends(get_db_session),
):
    """Get storyboard by ID."""
    service = StoryboardService(db)
    storyboard = service.get(storyboard_id)
    if not storyboard:
        raise HTTPException(status_code=404, detail="Storyboard not found")
    return BaseResponse(data=_storyboard_to_response(storyboard))


@router.put("/{storyboard_id}", response_model=BaseResponse[StoryboardResponse])
def update_storyboard(
    storyboard_id: int,
    schema: StoryboardUpdate,
    db: Session = Depends(get_db_session),
):
    """Update a storyboard."""
    service = StoryboardService(db)
    storyboard = service.update(storyboard_id, schema)
    if not storyboard:
        raise HTTPException(status_code=404, detail="Storyboard not found")
    return BaseResponse(data=_storyboard_to_response(storyboard))


@router.delete("/{storyboard_id}", response_model=BaseResponse[dict])
def delete_storyboard(
    storyboard_id: int,
    db: Session = Depends(get_db_session),
):
    """Delete a storyboard."""
    service = StoryboardService(db)
    success = service.delete(storyboard_id)
    if not success:
        raise HTTPException(status_code=404, detail="Storyboard not found")
    return BaseResponse(data={"id": storyboard_id, "deleted": True})


@router.post("/{storyboard_id}/characters", response_model=BaseResponse[StoryboardResponse])
def link_characters(
    storyboard_id: int,
    schema: StoryboardCharacterLink,
    episode_id: int = Query(...),
    project_id: int = Query(...),
    db: Session = Depends(get_db_session),
):
    """Link characters to a storyboard."""
    service = StoryboardService(db)
    storyboard = service.link_characters(
        storyboard_id,
        schema.character_ids,
        project_id,
        episode_id,
    )
    if not storyboard:
        raise HTTPException(status_code=404, detail="Storyboard not found")
    return BaseResponse(data=_storyboard_to_response(storyboard))


@router.post("/{storyboard_id}/scene", response_model=BaseResponse[StoryboardResponse])
def link_scene(
    storyboard_id: int,
    schema: StoryboardSceneLink,
    episode_id: int = Query(...),
    project_id: int = Query(...),
    db: Session = Depends(get_db_session),
):
    """Link scene to a storyboard."""
    service = StoryboardService(db)
    storyboard = service.link_scene(
        storyboard_id,
        schema.scene_id,
        project_id,
        episode_id,
    )
    if not storyboard:
        raise HTTPException(status_code=404, detail="Storyboard not found")
    return BaseResponse(data=_storyboard_to_response(storyboard))


@router.post("/{storyboard_id}/generate", response_model=BaseResponse[StoryboardListResponse])
def generate_storyboards(
    episode_id: int,
    model_instance_id: Optional[int] = None,
    use_vector: bool = False,
    db: Session = Depends(get_db_session),
):
    """Generate storyboards from episode content."""
    # Placeholder - would call LLM service here
    # This is a stub that returns empty results
    return BaseResponse(data=StoryboardListResponse(
        items=[],
        total=0,
        page=1,
        page_size=10,
    ))
