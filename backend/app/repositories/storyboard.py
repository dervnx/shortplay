from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.storyboard import Storyboard, StoryboardCharacter, StoryboardScene
from app.repositories.base import BaseRepository


class StoryboardRepository(BaseRepository[Storyboard]):
    """Repository for Storyboard model."""

    def __init__(self, db: Session):
        super().__init__(Storyboard, db)

    def get_by_episode(self, episode_id: int) -> List[Storyboard]:
        """Get all storyboards for an episode."""
        return self.db.query(Storyboard).filter(
            Storyboard.episode_id == episode_id,
            Storyboard.is_deleted == 0
        ).order_by(Storyboard.shot_number).all()

    def get_by_episode_paginated(
        self,
        episode_id: int,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[List[Storyboard], int]:
        """Get paginated storyboards for an episode."""
        query = self.db.query(Storyboard).filter(
            Storyboard.episode_id == episode_id,
            Storyboard.is_deleted == 0
        )
        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(Storyboard.shot_number).offset(offset).limit(page_size).all()
        return items, total

    def get_next_shot_number(self, episode_id: int) -> int:
        """Get next shot number for an episode."""
        from sqlalchemy import func
        result = self.db.query(func.max(Storyboard.shot_number)).filter(
            Storyboard.episode_id == episode_id,
            Storyboard.is_deleted == 0
        ).scalar()
        return (result or 0) + 1

    def update_thumbnail(self, id: int, thumbnail: str) -> Optional[Storyboard]:
        """Update storyboard thumbnail."""
        return self.update(id, thumbnail=thumbnail)

    def update_video_url(self, id: int, video_url: str) -> Optional[Storyboard]:
        """Update storyboard video URL."""
        return self.update(id, video_url=video_url)


class StoryboardCharacterRepository:
    """Repository for StoryboardCharacter association."""

    def __init__(self, db: Session):
        self.db = db

    def link_characters(self, storyboard_id: int, character_ids: List[int], project_id: int, episode_id: int) -> None:
        """Link characters to a storyboard."""
        # Delete existing links
        self.db.query(StoryboardCharacter).filter(
            StoryboardCharacter.storyboard_id == storyboard_id,
            StoryboardCharacter.is_deleted == 0
        ).delete()

        # Create new links
        for char_id in character_ids[:3]:  # Max 3 characters
            link = StoryboardCharacter(
                storyboard_id=storyboard_id,
                character_id=char_id,
                project_id=project_id,
                episode_id=episode_id,
            )
            self.db.add(link)
        self.db.commit()

    def get_characters(self, storyboard_id: int) -> List[dict]:
        """Get characters linked to a storyboard."""
        from app.models.character import Character
        results = self.db.query(StoryboardCharacter, Character).join(
            Character, StoryboardCharacter.character_id == Character.id
        ).filter(
            StoryboardCharacter.storyboard_id == storyboard_id,
            StoryboardCharacter.is_deleted == 0,
            Character.is_deleted == 0
        ).all()

        return [
            {"id": c.id, "name": c.name, "description": c.description}
            for sc, c in results
        ]


class StoryboardSceneRepository:
    """Repository for StoryboardScene association."""

    def __init__(self, db: Session):
        self.db = db

    def link_scene(self, storyboard_id: int, scene_id: int, project_id: int, episode_id: int) -> None:
        """Link scene to a storyboard."""
        # Delete existing links
        self.db.query(StoryboardScene).filter(
            StoryboardScene.storyboard_id == storyboard_id,
            StoryboardScene.is_deleted == 0
        ).delete()

        # Create new link
        link = StoryboardScene(
            storyboard_id=storyboard_id,
            scene_id=scene_id,
            project_id=project_id,
            episode_id=episode_id,
        )
        self.db.add(link)
        self.db.commit()

    def get_scene(self, storyboard_id: int) -> Optional[dict]:
        """Get scene linked to a storyboard."""
        from app.models.scene import Scene
        result = self.db.query(StoryboardScene, Scene).join(
            Scene, StoryboardScene.scene_id == Scene.id
        ).filter(
            StoryboardScene.storyboard_id == storyboard_id,
            StoryboardScene.is_deleted == 0,
            Scene.is_deleted == 0
        ).first()

        if result:
            sc, s = result
            return {"id": s.id, "name": s.name, "description": s.description}
        return None
