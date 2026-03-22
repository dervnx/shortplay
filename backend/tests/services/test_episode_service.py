import pytest
from sqlalchemy.orm import Session

from app.services.episode_service import EpisodeService
from app.services.project_service import ProjectService
from app.schemas.episode import EpisodeCreate, EpisodeUpdate
from app.schemas.project import ProjectCreate


class TestEpisodeService:
    """Tests for EpisodeService."""

    def _create_project(self, db: Session, name: str = "测试项目") -> int:
        """Helper to create a project."""
        service = ProjectService(db)
        project = service.create(ProjectCreate(name=name))
        return project.id

    def test_create_episode(self, db: Session):
        """Test creating an episode via service."""
        project_id = self._create_project(db)
        service = EpisodeService(db)
        schema = EpisodeCreate(name="第一章", content="内容", chapter_number=1)

        episode = service.create(project_id, schema)

        assert episode.id is not None
        assert episode.name == "第一章"
        assert episode.project_id == project_id
        assert episode.current_step == 0

    def test_get_episode(self, db: Session):
        """Test getting an episode via service."""
        project_id = self._create_project(db)
        service = EpisodeService(db)
        created = service.create(project_id, EpisodeCreate(name="第一章", chapter_number=1))

        retrieved = service.get(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id

    def test_list_by_project(self, db: Session):
        """Test listing episodes by project."""
        project_id = self._create_project(db)
        service = EpisodeService(db)

        service.create(project_id, EpisodeCreate(name="第一章", chapter_number=1))
        service.create(project_id, EpisodeCreate(name="第二章", chapter_number=2))

        result = service.list_by_project(project_id)

        assert result.total == 2
        assert len(result.items) == 2

    def test_update_episode(self, db: Session):
        """Test updating an episode via service."""
        project_id = self._create_project(db)
        service = EpisodeService(db)
        created = service.create(project_id, EpisodeCreate(name="原始", chapter_number=1))

        updated = service.update(created.id, EpisodeUpdate(name="新名称", current_step=2))

        assert updated.name == "新名称"
        assert updated.current_step == 2

    def test_delete_episode(self, db: Session):
        """Test deleting an episode via service."""
        project_id = self._create_project(db)
        service = EpisodeService(db)
        created = service.create(project_id, EpisodeCreate(name="待删除", chapter_number=1))

        result = service.delete(created.id)

        assert result is True
        assert service.get(created.id) is None

    def test_update_step(self, db: Session):
        """Test updating episode current step."""
        project_id = self._create_project(db)
        service = EpisodeService(db)
        created = service.create(project_id, EpisodeCreate(name="测试", chapter_number=1))

        updated = service.update_step(created.id, 3)

        assert updated.current_step == 3
