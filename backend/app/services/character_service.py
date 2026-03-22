from __future__ import annotations
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterUpdate
from app.schemas.common import PaginatedResponse
from app.repositories.character import CharacterRepository


class CharacterService:
    """Service for character business logic."""

    def __init__(self, db: Session):
        self.repo = CharacterRepository(db)

    def create(self, project_id: int, schema: CharacterCreate) -> Character:
        """Create a new character."""
        return self.repo.create(
            project_id=project_id,
            episode_id=schema.episode_id,
            name=schema.name,
            description=schema.description,
        )

    def get(self, id: int) -> Optional[Character]:
        """Get character by ID."""
        return self.repo.get(id)

    def list_by_project(
        self,
        project_id: int,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedResponse[Character]:
        """List characters for a project."""
        items, total = self.repo.search(
            project_id=project_id,
            keyword=keyword,
            page=page,
            page_size=page_size,
        )
        return PaginatedResponse.create(items, total, page, page_size)

    def list_by_episode(self, episode_id: int) -> List[Character]:
        """List characters for an episode."""
        return self.repo.get_by_episode(episode_id)

    def update(self, id: int, schema: CharacterUpdate) -> Optional[Character]:
        """Update a character."""
        update_data = schema.model_dump(exclude_unset=True)
        return self.repo.update(id, **update_data)

    def delete(self, id: int) -> bool:
        """Delete a character."""
        return self.repo.delete(id)

    def update_avatar(self, id: int, avatar: str) -> Optional[Character]:
        """Update character avatar."""
        return self.repo.update_avatar(id, avatar)

    def bulk_create(self, project_id: int, episode_id: int, characters: List[dict]) -> List[Character]:
        """Bulk create characters."""
        results = []
        for char_data in characters:
            char = self.repo.create(
                project_id=project_id,
                episode_id=episode_id,
                name=char_data["name"],
                description=char_data.get("description"),
            )
            results.append(char)
        return results
