from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.storyboard import Storyboard
from app.schemas.storyboard import StoryboardCreate, StoryboardUpdate
from app.schemas.common import PaginatedResponse
from app.repositories.storyboard import (
    StoryboardRepository,
    StoryboardCharacterRepository,
    StoryboardSceneRepository,
)


class StoryboardService:
    """Service for storyboard business logic."""

    def __init__(self, db: Session):
        self.repo = StoryboardRepository(db)
        self.char_repo = StoryboardCharacterRepository(db)
        self.scene_repo = StoryboardSceneRepository(db)

    def _enrich_storyboard(self, storyboard: Storyboard) -> dict:
        """Enrich storyboard with character and scene data."""
        characters = self.char_repo.get_characters(storyboard.id)
        scene = self.scene_repo.get_scene(storyboard.id)

        return {
            "id": storyboard.id,
            "episode_id": storyboard.episode_id,
            "shot_number": storyboard.shot_number,
            "shot_type": storyboard.shot_type,
            "duration": storyboard.duration,
            "description": storyboard.description,
            "dialogue": storyboard.dialogue,
            "thumbnail": storyboard.thumbnail,
            "video_url": storyboard.video_url,
            "image_prompt": storyboard.image_prompt,
            "video_prompt": storyboard.video_prompt,
            "order_index": storyboard.order_index,
            "characters": characters,
            "scene": scene,
            "created_at": storyboard.created_at,
            "updated_at": storyboard.updated_at,
        }

    def get(self, id: int) -> Optional[dict]:
        """Get storyboard by ID with related data."""
        storyboard = self.repo.get(id)
        if storyboard:
            return self._enrich_storyboard(storyboard)
        return None

    def list_by_episode(self, episode_id: int) -> List[dict]:
        """List storyboards for an episode with related data."""
        storyboards = self.repo.get_by_episode(episode_id)
        return [self._enrich_storyboard(sb) for sb in storyboards]

    def create(self, episode_id: int, schema: StoryboardCreate) -> dict:
        """Create a new storyboard."""
        shot_number = schema.shot_number or self.repo.get_next_shot_number(episode_id)
        storyboard = self.repo.create(
            episode_id=episode_id,
            shot_number=shot_number,
            description=schema.description,
            shot_type=schema.shot_type,
            duration=schema.duration,
            dialogue=schema.dialogue,
        )
        return self._enrich_storyboard(storyboard)

    def update(self, id: int, schema: StoryboardUpdate) -> Optional[dict]:
        """Update a storyboard."""
        update_data = schema.model_dump(exclude_unset=True)
        storyboard = self.repo.update(id, **update_data)
        if storyboard:
            return self._enrich_storyboard(storyboard)
        return None

    def delete(self, id: int) -> bool:
        """Delete a storyboard."""
        return self.repo.delete(id)

    def link_characters(self, id: int, character_ids: List[int], project_id: int, episode_id: int) -> dict:
        """Link characters to a storyboard."""
        self.char_repo.link_characters(id, character_ids, project_id, episode_id)
        return self.get(id)

    def link_scene(self, id: int, scene_id: int, project_id: int, episode_id: int) -> dict:
        """Link scene to a storyboard."""
        self.scene_repo.link_scene(id, scene_id, project_id, episode_id)
        return self.get(id)

    def update_thumbnail(self, id: int, thumbnail: str) -> Optional[dict]:
        """Update storyboard thumbnail."""
        self.repo.update_thumbnail(id, thumbnail)
        return self.get(id)

    def update_video_url(self, id: int, video_url: str) -> Optional[dict]:
        """Update storyboard video URL."""
        self.repo.update_video_url(id, video_url)
        return self.get(id)

    def bulk_create(self, episode_id: int, storyboards: List[dict]) -> List[dict]:
        """Bulk create storyboards."""
        results = []
        for i, sb_data in enumerate(storyboards):
            storyboard = self.repo.create(
                episode_id=episode_id,
                shot_number=sb_data.get("shot_number", i + 1),
                description=sb_data["description"],
                shot_type=sb_data.get("shot_type", 1),
                duration=sb_data.get("duration", 5),
            )
            results.append(self._enrich_storyboard(storyboard))
        return results
