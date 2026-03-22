from fastapi import APIRouter

from app.api.v1 import (
    projects,
    episodes,
    characters,
    scenes,
    storyboards,
    models,
    prompts,
    providers,
    project_model,
)

api_router = APIRouter()


@api_router.get("/health")
def health_check():
    return {"status": "healthy"}


api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(episodes.router, prefix="/episodes", tags=["episodes"])
api_router.include_router(characters.router, prefix="/characters", tags=["characters"])
api_router.include_router(scenes.router, prefix="/scenes", tags=["scenes"])
api_router.include_router(storyboards.router, prefix="/storyboards", tags=["storyboards"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
api_router.include_router(providers.router, prefix="/providers", tags=["providers"])
api_router.include_router(project_model.router, prefix="", tags=["project-model"])
