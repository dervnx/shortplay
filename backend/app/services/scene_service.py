from __future__ import annotations
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.scene import Scene
from app.schemas.scene import SceneCreate, SceneUpdate
from app.schemas.common import PaginatedResponse
from app.repositories.scene import SceneRepository


class SceneService:
    """Service for scene business logic."""

    def __init__(self, db: Session):
        self.repo = SceneRepository(db)

    def create(self, project_id: int, schema: SceneCreate) -> Scene:
        """Create a new scene."""
        return self.repo.create(
            project_id=project_id,
            episode_id=schema.episode_id,
            name=schema.name,
            description=schema.description,
        )

    def get(self, id: int) -> Optional[Scene]:
        """Get scene by ID."""
        return self.repo.get(id)

    def list_by_project(
        self,
        project_id: int,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedResponse[Scene]:
        """List scenes for a project."""
        items, total = self.repo.search(
            project_id=project_id,
            keyword=keyword,
            page=page,
            page_size=page_size,
        )
        return PaginatedResponse.create(items, total, page, page_size)

    def list_by_episode(self, episode_id: int) -> List[Scene]:
        """List scenes for an episode."""
        return self.repo.get_by_episode(episode_id)

    def update(self, id: int, schema: SceneUpdate) -> Optional[Scene]:
        """Update a scene."""
        update_data = schema.model_dump(exclude_unset=True)
        return self.repo.update(id, **update_data)

    def delete(self, id: int) -> bool:
        """Delete a scene."""
        return self.repo.delete(id)

    def update_thumbnail(self, id: int, thumbnail: str) -> Optional[Scene]:
        """Update scene thumbnail."""
        return self.repo.update_thumbnail(id, thumbnail)

    def bulk_create(self, project_id: int, episode_id: int, scenes: List[dict]) -> List[Scene]:
        """Bulk create scenes."""
        results = []
        for scene_data in scenes:
            scene = self.repo.create(
                project_id=project_id,
                episode_id=episode_id,
                name=scene_data["name"],
                description=scene_data.get("description"),
            )
            results.append(scene)
        return results
