from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_session
from app.schemas.common import BaseResponse
from app.schemas.prompt import (
    PromptTemplateCreate,
    PromptTemplateUpdate,
    PromptTemplateResponse,
    PromptTemplateListResponse,
)
from app.repositories.base import BaseRepository
from app.models.prompt_template import PromptTemplate

router = APIRouter()


class PromptTemplateRepository(BaseRepository[PromptTemplate]):
    """Repository for PromptTemplate model."""

    def __init__(self, db: Session):
        super().__init__(PromptTemplate, db)

    def get_by_scene(self, scene_code: int) -> List[PromptTemplate]:
        """Get templates by scene code."""
        return self.db.query(PromptTemplate).filter(
            PromptTemplate.scene_code == scene_code,
            PromptTemplate.is_deleted == 0
        ).all()


def get_repo(db: Session) -> PromptTemplateRepository:
    return PromptTemplateRepository(db)


@router.get("", response_model=BaseResponse[PromptTemplateListResponse])
def list_templates(
    scene_code: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_session),
):
    """List prompt templates."""
    repo = get_repo(db)
    if scene_code:
        items = repo.get_by_scene(scene_code)
        total = len(items)
    else:
        items, total = repo.paginate(page, page_size)
    return BaseResponse(data=PromptTemplateListResponse(
        items=[PromptTemplateResponse.model_validate(t) for t in items],
        total=total,
        page=page,
        page_size=page_size,
    ))


@router.post("", response_model=BaseResponse[PromptTemplateResponse])
def create_template(
    schema: PromptTemplateCreate,
    db: Session = Depends(get_db_session),
):
    """Create a new prompt template."""
    repo = get_repo(db)
    template = repo.create(
        prompt_code=schema.prompt_code,
        prompt_name=schema.prompt_name,
        scene_code=schema.scene_code,
        prompt_content=schema.prompt_content,
    )
    return BaseResponse(data=PromptTemplateResponse.model_validate(template))


@router.get("/{template_id}", response_model=BaseResponse[PromptTemplateResponse])
def get_template(
    template_id: int,
    db: Session = Depends(get_db_session),
):
    """Get prompt template by ID."""
    repo = get_repo(db)
    template = repo.get(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return BaseResponse(data=PromptTemplateResponse.model_validate(template))


@router.put("/{template_id}", response_model=BaseResponse[PromptTemplateResponse])
def update_template(
    template_id: int,
    schema: PromptTemplateUpdate,
    db: Session = Depends(get_db_session),
):
    """Update a prompt template."""
    repo = get_repo(db)
    update_data = schema.model_dump(exclude_unset=True)
    template = repo.update(template_id, **update_data)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return BaseResponse(data=PromptTemplateResponse.model_validate(template))


@router.delete("/{template_id}", response_model=BaseResponse[dict])
def delete_template(
    template_id: int,
    db: Session = Depends(get_db_session),
):
    """Delete a prompt template."""
    repo = get_repo(db)
    success = repo.delete(template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    return BaseResponse(data={"id": template_id, "deleted": True})
