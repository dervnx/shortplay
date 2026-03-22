# Schemas module
from app.schemas.common import BaseResponse, PaginatedResponse, PageParams
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
    ExtractionResponse,
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
from app.schemas.storyboard import (
    StoryboardCreate,
    StoryboardUpdate,
    StoryboardResponse,
    StoryboardGenerate,
    StoryboardCharacterLink,
    StoryboardSceneLink,
)
from app.schemas.model import (
    ModelDefinitionCreate,
    ModelDefinitionResponse,
    ModelInstanceCreate,
    ModelInstanceUpdate,
    ModelInstanceResponse,
)
from app.schemas.prompt import (
    PromptTemplateCreate,
    PromptTemplateUpdate,
    PromptTemplateResponse,
)

__all__ = [
    "BaseResponse",
    "PaginatedResponse",
    "PageParams",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectListResponse",
    "EpisodeCreate",
    "EpisodeUpdate",
    "EpisodeResponse",
    "EpisodeListResponse",
    "ExtractionResponse",
    "CharacterCreate",
    "CharacterUpdate",
    "CharacterResponse",
    "CharacterListResponse",
    "SceneCreate",
    "SceneUpdate",
    "SceneResponse",
    "SceneListResponse",
    "StoryboardCreate",
    "StoryboardUpdate",
    "StoryboardResponse",
    "StoryboardGenerate",
    "StoryboardCharacterLink",
    "StoryboardSceneLink",
    "ModelDefinitionCreate",
    "ModelDefinitionResponse",
    "ModelInstanceCreate",
    "ModelInstanceUpdate",
    "ModelInstanceResponse",
    "PromptTemplateCreate",
    "PromptTemplateUpdate",
    "PromptTemplateResponse",
]
