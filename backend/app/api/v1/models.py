from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db_session
from app.schemas.common import BaseResponse
from app.schemas.model import (
    ModelDefinitionCreate,
    ModelDefinitionResponse,
    ModelInstanceCreate,
    ModelInstanceUpdate,
    ModelInstanceResponse,
    ModelInstanceListResponse,
)
from app.services.model_service import ModelService

router = APIRouter()


# Model Definitions
@router.get("/definitions", response_model=BaseResponse[List[ModelDefinitionResponse]])
def list_definitions(
    db: Session = Depends(get_db_session),
):
    """List all model definitions."""
    service = ModelService(db)
    definitions = service.list_definitions()
    return BaseResponse(data=[ModelDefinitionResponse.model_validate(d) for d in definitions])


@router.post("/definitions", response_model=BaseResponse[ModelDefinitionResponse])
def create_definition(
    schema: ModelDefinitionCreate,
    db: Session = Depends(get_db_session),
):
    """Create a new model definition."""
    service = ModelService(db)
    definition = service.create_definition(schema)
    return BaseResponse(data=ModelDefinitionResponse.model_validate(definition))


# Model Instances
@router.get("/instances", response_model=BaseResponse[ModelInstanceListResponse])
def list_instances(
    model_type: Optional[int] = None,
    scene_code: Optional[int] = None,
    provider_id: Optional[int] = None,
    db: Session = Depends(get_db_session),
):
    """List model instances with filters."""
    service = ModelService(db)
    instances = service.list_instances(model_type=model_type, scene_code=scene_code, provider_id=provider_id)
    return BaseResponse(data=ModelInstanceListResponse(
        items=[ModelInstanceResponse.model_validate(i) for i in instances],
        total=len(instances),
        page=1,
        page_size=len(instances),
    ))


@router.post("/instances", response_model=BaseResponse[ModelInstanceResponse])
def create_instance(
    schema: ModelInstanceCreate,
    db: Session = Depends(get_db_session),
):
    """Create a new model instance."""
    service = ModelService(db)
    instance = service.create_instance(schema)
    return BaseResponse(data=ModelInstanceResponse.model_validate(instance))


@router.get("/instances/{instance_id}", response_model=BaseResponse[ModelInstanceResponse])
def get_instance(
    instance_id: int,
    db: Session = Depends(get_db_session),
):
    """Get model instance by ID."""
    service = ModelService(db)
    instance = service.get_instance(instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Model instance not found")
    return BaseResponse(data=ModelInstanceResponse.model_validate(instance))


@router.put("/instances/{instance_id}", response_model=BaseResponse[ModelInstanceResponse])
def update_instance(
    instance_id: int,
    schema: ModelInstanceUpdate,
    db: Session = Depends(get_db_session),
):
    """Update a model instance."""
    service = ModelService(db)
    instance = service.update_instance(instance_id, schema)
    if not instance:
        raise HTTPException(status_code=404, detail="Model instance not found")
    return BaseResponse(data=ModelInstanceResponse.model_validate(instance))


@router.delete("/instances/{instance_id}", response_model=BaseResponse[dict])
def delete_instance(
    instance_id: int,
    db: Session = Depends(get_db_session),
):
    """Delete a model instance."""
    service = ModelService(db)
    success = service.delete_instance(instance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Model instance not found")
    return BaseResponse(data={"id": instance_id, "deleted": True})


@router.put("/instances/{instance_id}/default", response_model=BaseResponse[dict])
def set_default_instance(
    instance_id: int,
    model_type: int = Query(...),
    db: Session = Depends(get_db_session),
):
    """Set default model instance for a type."""
    service = ModelService(db)
    service.set_default(instance_id, model_type)
    return BaseResponse(data={"model_type": model_type, "instance_id": instance_id})


@router.get("/instances/default", response_model=BaseResponse[dict])
def get_defaults_by_type(
    model_type: int = Query(...),
    db: Session = Depends(get_db_session),
):
    """Get default model instance for a type."""
    service = ModelService(db)
    defaults = service.get_defaults_by_type()
    instance = defaults.get(model_type)
    if not instance:
        raise HTTPException(status_code=404, detail="No default model instance found for type")
    return BaseResponse(data={"model_type": model_type, "instance": ModelInstanceResponse.model_validate(instance)})
