from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.scene import Scene
from app.repositories.base import BaseRepository


class SceneRepository(BaseRepository[Scene]):
    """Repository for Scene model."""

    def __init__(self, db: Session):
        super().__init__(Scene, db)

    def get_by_project(self, project_id: int) -> List[Scene]:
        """Get all scenes for a project."""
        return self.db.query(Scene).filter(
            Scene.project_id == project_id,
            Scene.is_deleted == 0
        ).all()

    def get_by_episode(self, episode_id: int) -> List[Scene]:
        """Get all scenes for an episode."""
        return self.db.query(Scene).filter(
            Scene.episode_id == episode_id,
            Scene.is_deleted == 0
        ).all()

    def get_by_ids(self, ids: List[int]) -> List[Scene]:
        """Get scenes by IDs."""
        return self.db.query(Scene).filter(
            Scene.id.in_(ids),
            Scene.is_deleted == 0
        ).all()

    def search(
        self,
        project_id: int,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[List[Scene], int]:
        """Search scenes within a project."""
        query = self.db.query(Scene).filter(
            Scene.project_id == project_id,
            Scene.is_deleted == 0
        )

        if keyword:
            query = query.filter(Scene.name.ilike(f"%{keyword}%"))

        total = query.count()
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return items, total

    def update_thumbnail(self, id: int, thumbnail: str) -> Optional[Scene]:
        """Update scene thumbnail."""
        return self.update(id, thumbnail=thumbnail)
