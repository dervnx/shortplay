import pytest
from sqlalchemy.orm import Session

from app.services.storyboard_service import StoryboardService
from app.services.scene_service import SceneService
from app.services.project_service import ProjectService
from app.services.episode_service import EpisodeService
from app.schemas.storyboard import StoryboardCreate
from app.schemas.scene import SceneCreate
from app.schemas.episode import EpisodeCreate
from app.schemas.project import ProjectCreate


class TestStoryboardService:
    """Tests for StoryboardService."""

    def _create_project_episode(self, db: Session):
        """Helper to create project and episode."""
        project_service = ProjectService(db)
        project = project_service.create(ProjectCreate(name="测试项目"))
        episode_service = EpisodeService(db)
        episode = episode_service.create(project.id, EpisodeCreate(name="第一章", chapter_number=1))
        return project.id, episode.id

    def test_create_storyboard(self, db: Session):
        """Test creating a storyboard via service."""
        project_id, episode_id = self._create_project_episode(db)
        service = StoryboardService(db)
        schema = StoryboardCreate(
            episode_id=episode_id,
            shot_number=1,
            shot_type=1,
            duration=5,
            description="测试镜头"
        )

        storyboard = service.create(episode_id, schema)

        assert storyboard["id"] is not None
        assert storyboard["description"] == "测试镜头"
        assert storyboard["episode_id"] == episode_id

    def test_get_storyboard(self, db: Session):
        """Test getting a storyboard via service."""
        project_id, episode_id = self._create_project_episode(db)
        service = StoryboardService(db)
        created = service.create(episode_id, StoryboardCreate(
            episode_id=episode_id, shot_number=1, shot_type=1, duration=5, description="测试"
        ))

        retrieved = service.get(created["id"])

        assert retrieved is not None
        assert retrieved["id"] == created["id"]

    def test_list_by_episode(self, db: Session):
        """Test listing storyboards by episode."""
        project_id, episode_id = self._create_project_episode(db)
        service = StoryboardService(db)

        service.create(episode_id, StoryboardCreate(episode_id=episode_id, shot_number=1, shot_type=1, duration=5, description="测试1"))
        service.create(episode_id, StoryboardCreate(episode_id=episode_id, shot_number=2, shot_type=1, duration=5, description="测试2"))

        storyboards = service.list_by_episode(episode_id)

        assert len(storyboards) == 2

    def test_update_storyboard(self, db: Session):
        """Test updating a storyboard via service."""
        project_id, episode_id = self._create_project_episode(db)
        service = StoryboardService(db)
        from app.schemas.storyboard import StoryboardUpdate
        created = service.create(episode_id, StoryboardCreate(
            episode_id=episode_id, shot_number=1, shot_type=1, duration=5, description="原始"
        ))

        updated = service.update(created["id"], StoryboardUpdate(description="更新后"))

        assert updated["description"] == "更新后"

    def test_delete_storyboard(self, db: Session):
        """Test deleting a storyboard via service."""
        project_id, episode_id = self._create_project_episode(db)
        service = StoryboardService(db)
        created = service.create(episode_id, StoryboardCreate(
            episode_id=episode_id, shot_number=1, shot_type=1, duration=5, description="测试"
        ))

        result = service.delete(created["id"])

        assert result is True
        assert service.get(created["id"]) is None
