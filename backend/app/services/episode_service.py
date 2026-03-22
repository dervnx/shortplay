from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.episode import Episode
from app.schemas.episode import EpisodeCreate, EpisodeUpdate
from app.schemas.common import PaginatedResponse
from app.repositories.episode import EpisodeRepository
from app.repositories.project import ProjectRepository


class EpisodeService:
    """Service for episode business logic."""

    def __init__(self, db: Session):
        self.repo = EpisodeRepository(db)
        self.project_repo = ProjectRepository(db)

    def create(self, project_id: int, schema: EpisodeCreate) -> Episode:
        """Create a new episode."""
        chapter_number = schema.chapter_number or self.repo.get_next_chapter_number(project_id)
        return self.repo.create(
            project_id=project_id,
            chapter_number=chapter_number,
            name=schema.name,
            content=schema.content,
            status=0,
            progress=0,
            current_step=0,
        )

    def get(self, id: int) -> Optional[Episode]:
        """Get episode by ID."""
        return self.repo.get(id)

    def list_by_project(
        self,
        project_id: int,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedResponse[Episode]:
        """List episodes for a project."""
        items, total = self.repo.get_by_project_paginated(
            project_id=project_id,
            page=page,
            page_size=page_size,
        )
        return PaginatedResponse.create(items, total, page, page_size)

    def update(self, id: int, schema: EpisodeUpdate) -> Optional[Episode]:
        """Update an episode."""
        update_data = schema.model_dump(exclude_unset=True)
        return self.repo.update(id, **update_data)

    def delete(self, id: int) -> bool:
        """Delete an episode."""
        episode = self.repo.get(id)
        if episode:
            project_id = episode.project_id
            result = self.repo.delete(id)
            # Decrement project chapter count
            self.project_repo.decrement_chapter_count(project_id)
            return result
        return False

    def update_step(self, id: int, current_step: int) -> Optional[Episode]:
        """Update episode current step."""
        return self.repo.update_step(id, current_step)
