from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_session
from app.schemas.common import BaseResponse
from app.schemas.character import (
    CharacterCreate,
    CharacterUpdate,
    CharacterResponse,
    CharacterListResponse,
)
from app.services.character_service import CharacterService

router = APIRouter()


@router.get("/projects/{project_id}/characters", response_model=BaseResponse[CharacterListResponse])
def list_characters(
    project_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db_session),
):
    """List characters for a project."""
    service = CharacterService(db)
    result = service.list_by_project(project_id, keyword, page, page_size)
    items = [CharacterResponse.model_validate(c) for c in result.items]
    return BaseResponse(data=CharacterListResponse(
        items=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    ))


@router.post("/projects/{project_id}/characters", response_model=BaseResponse[CharacterResponse])
def create_character(
    project_id: int,
    schema: CharacterCreate,
    db: Session = Depends(get_db_session),
):
    """Create a new character."""
    service = CharacterService(db)
    # Override project_id from path
    schema.episode_id = schema.episode_id  # Keep from body
    character = service.create(project_id, schema)
    return BaseResponse(data=CharacterResponse.model_validate(character))


@router.get("/{character_id}", response_model=BaseResponse[CharacterResponse])
def get_character(
    character_id: int,
    db: Session = Depends(get_db_session),
):
    """Get character by ID."""
    service = CharacterService(db)
    character = service.get(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return BaseResponse(data=CharacterResponse.model_validate(character))


@router.put("/{character_id}", response_model=BaseResponse[CharacterResponse])
def update_character(
    character_id: int,
    schema: CharacterUpdate,
    db: Session = Depends(get_db_session),
):
    """Update a character."""
    service = CharacterService(db)
    character = service.update(character_id, schema)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return BaseResponse(data=CharacterResponse.model_validate(character))


@router.delete("/{character_id}", response_model=BaseResponse[dict])
def delete_character(
    character_id: int,
    db: Session = Depends(get_db_session),
):
    """Delete a character."""
    service = CharacterService(db)
    success = service.delete(character_id)
    if not success:
        raise HTTPException(status_code=404, detail="Character not found")
    return BaseResponse(data={"id": character_id, "deleted": True})


@router.post("/{character_id}/avatar", response_model=BaseResponse[CharacterResponse])
def update_character_avatar(
    character_id: int,
    avatar: str,
    db: Session = Depends(get_db_session),
):
    """Update character avatar URL."""
    service = CharacterService(db)
    character = service.update_avatar(character_id, avatar)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return BaseResponse(data=CharacterResponse.model_validate(character))
