from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.character import Character
from app.repositories.base import BaseRepository


class CharacterRepository(BaseRepository[Character]):
    """Repository for Character model."""

    def __init__(self, db: Session):
        super().__init__(Character, db)

    def get_by_project(self, project_id: int) -> List[Character]:
        """Get all characters for a project."""
        return self.db.query(Character).filter(
            Character.project_id == project_id,
            Character.is_deleted == 0
        ).all()

    def get_by_episode(self, episode_id: int) -> List[Character]:
        """Get all characters for an episode."""
        return self.db.query(Character).filter(
            Character.episode_id == episode_id,
            Character.is_deleted == 0
        ).all()

    def get_by_ids(self, ids: List[int]) -> List[Character]:
        """Get characters by IDs."""
        return self.db.query(Character).filter(
            Character.id.in_(ids),
            Character.is_deleted == 0
        ).all()

    def search(
        self,
        project_id: int,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[List[Character], int]:
        """Search characters within a project."""
        query = self.db.query(Character).filter(
            Character.project_id == project_id,
            Character.is_deleted == 0
        )

        if keyword:
            query = query.filter(Character.name.ilike(f"%{keyword}%"))

        total = query.count()
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return items, total

    def update_avatar(self, id: int, avatar: str) -> Optional[Character]:
        """Update character avatar."""
        return self.update(id, avatar=avatar)
