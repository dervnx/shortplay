from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.episode import Episode
from app.repositories.base import BaseRepository


class EpisodeRepository(BaseRepository[Episode]):
    """Repository for Episode model."""

    def __init__(self, db: Session):
        super().__init__(Episode, db)

    def get_by_project(self, project_id: int) -> List[Episode]:
        """Get all episodes for a project."""
        return self.db.query(Episode).filter(
            Episode.project_id == project_id,
            Episode.is_deleted == 0
        ).order_by(Episode.chapter_number).all()

    def get_by_project_paginated(
        self,
        project_id: int,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[List[Episode], int]:
        """Get paginated episodes for a project."""
        query = self.db.query(Episode).filter(
            Episode.project_id == project_id,
            Episode.is_deleted == 0
        )
        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(Episode.chapter_number).offset(offset).limit(page_size).all()
        return items, total

    def get_next_chapter_number(self, project_id: int) -> int:
        """Get next chapter number for a project."""
        from sqlalchemy import func
        result = self.db.query(func.max(Episode.chapter_number)).filter(
            Episode.project_id == project_id,
            Episode.is_deleted == 0
        ).scalar()
        return (result or 0) + 1

    def update_step(self, id: int, current_step: int) -> Optional[Episode]:
        """Update episode current step."""
        return self.update(id, current_step=current_step)
