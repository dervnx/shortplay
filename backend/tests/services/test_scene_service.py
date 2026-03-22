import pytest
from sqlalchemy.orm import Session

from app.services.scene_service import SceneService
from app.services.project_service import ProjectService
from app.services.episode_service import EpisodeService
from app.schemas.scene import SceneCreate
from app.schemas.episode import EpisodeCreate
from app.schemas.project import ProjectCreate


class TestSceneService:
    """Tests for SceneService."""

    def _create_project_and_episode(self, db: Session):
        """Helper to create project and episode."""
        project_service = ProjectService(db)
        project = project_service.create(ProjectCreate(name="测试项目"))
        episode_service = EpisodeService(db)
        episode = episode_service.create(project.id, EpisodeCreate(name="第一章", chapter_number=1))
        return project.id, episode.id

    def test_create_scene(self, db: Session):
        """Test creating a scene via service."""
        project_id, episode_id = self._create_project_and_episode(db)
        service = SceneService(db)
        schema = SceneCreate(name="场景1", description="测试场景", episode_id=episode_id)

        scene = service.create(project_id, schema)

        assert scene.id is not None
        assert scene.name == "场景1"
        assert scene.episode_id == episode_id

    def test_get_scene(self, db: Session):
        """Test getting a scene via service."""
        project_id, episode_id = self._create_project_and_episode(db)
        service = SceneService(db)
        schema = SceneCreate(name="场景1", episode_id=episode_id)
        created = service.create(project_id, schema)

        retrieved = service.get(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id

    def test_list_by_episode(self, db: Session):
        """Test listing scenes by episode."""
        project_id, episode_id = self._create_project_and_episode(db)
        service = SceneService(db)

        service.create(project_id, SceneCreate(name="场景1", episode_id=episode_id))
        service.create(project_id, SceneCreate(name="场景2", episode_id=episode_id))

        scenes = service.list_by_episode(episode_id)

        assert len(scenes) == 2

    def test_delete_scene(self, db: Session):
        """Test deleting a scene via service."""
        project_id, episode_id = self._create_project_and_episode(db)
        service = SceneService(db)
        created = service.create(project_id, SceneCreate(name="待删除", episode_id=episode_id))

        result = service.delete(created.id)

        assert result is True
        assert service.get(created.id) is None
