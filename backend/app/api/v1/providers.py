from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_session
from app.schemas.common import BaseResponse
from app.schemas.provider import ProviderCreate, ProviderUpdate, ProviderResponse
from app.models.model_provider import ModelProvider
from app.repositories.base import BaseRepository

router = APIRouter()


def get_provider_repo(db: Session):
    return BaseRepository(ModelProvider, db)


@router.get("", response_model=BaseResponse[List[ProviderResponse]])
def list_providers(db: Session = Depends(get_db_session)):
    """List all model providers."""
    repo = get_provider_repo(db)
    providers = repo.get_all()
    return BaseResponse(data=[ProviderResponse.model_validate(p) for p in providers])


@router.post("", response_model=BaseResponse[ProviderResponse])
def create_provider(schema: ProviderCreate, db: Session = Depends(get_db_session)):
    """Create a new model provider."""
    repo = get_provider_repo(db)
    provider = repo.create(**schema.model_dump())
    return BaseResponse(data=ProviderResponse.model_validate(provider))


@router.get("/{provider_id}", response_model=BaseResponse[ProviderResponse])
def get_provider(provider_id: int, db: Session = Depends(get_db_session)):
    """Get provider by ID."""
    repo = get_provider_repo(db)
    provider = repo.get(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return BaseResponse(data=ProviderResponse.model_validate(provider))


@router.put("/{provider_id}", response_model=BaseResponse[ProviderResponse])
def update_provider(provider_id: int, schema: ProviderUpdate, db: Session = Depends(get_db_session)):
    """Update a provider."""
    repo = get_provider_repo(db)
    provider = repo.get(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    update_data = schema.model_dump(exclude_unset=True)
    provider = repo.update(provider_id, **update_data)
    return BaseResponse(data=ProviderResponse.model_validate(provider))


@router.delete("/{provider_id}", response_model=BaseResponse[dict])
def delete_provider(provider_id: int, db: Session = Depends(get_db_session)):
    """Delete a provider."""
    repo = get_provider_repo(db)
    success = repo.delete(provider_id)
    if not success:
        raise HTTPException(status_code=404, detail="Provider not found")
    return BaseResponse(data={"id": provider_id, "deleted": True})
