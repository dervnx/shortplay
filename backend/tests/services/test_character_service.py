import pytest
from sqlalchemy.orm import Session

from app.services.character_service import CharacterService
from app.services.episode_service import EpisodeService
from app.services.project_service import ProjectService
from app.schemas.character import CharacterCreate, CharacterUpdate
from app.schemas.episode import EpisodeCreate
from app.schemas.project import ProjectCreate


class TestCharacterService:
    """Tests for CharacterService."""

    def _create_project_and_episode(self, db: Session) -> tuple:
        """Helper to create project and episode."""
        proj_service = ProjectService(db)
        project = proj_service.create(ProjectCreate(name="测试项目"))
        project_id = project.id

        ep_service = EpisodeService(db)
        episode = ep_service.create(project_id, EpisodeCreate(name="第一章", chapter_number=1))
        episode_id = episode.id

        return project_id, episode_id

    def test_create_character(self, db: Session):
        """Test creating a character via service."""
        project_id, episode_id = self._create_project_and_episode(db)
        service = CharacterService(db)
        schema = CharacterCreate(episode_id=episode_id, name="主角", description="故事主角")

        character = service.create(project_id, schema)

        assert character.id is not None
        assert character.name == "主角"
        assert character.project_id == project_id

    def test_get_character(self, db: Session):
        """Test getting a character via service."""
        project_id, episode_id = self._create_project_and_episode(db)
        service = CharacterService(db)
        created = service.create(project_id, CharacterCreate(episode_id=episode_id, name="主角"))

        retrieved = service.get(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id

    def test_list_by_project(self, db: Session):
        """Test listing characters by project."""
        project_id, episode_id = self._create_project_and_episode(db)
        service = CharacterService(db)

        service.create(project_id, CharacterCreate(episode_id=episode_id, name="角色1"))
        service.create(project_id, CharacterCreate(episode_id=episode_id, name="角色2"))

        result = service.list_by_project(project_id)

        assert result.total == 2

    def test_update_character(self, db: Session):
        """Test updating a character via service."""
        project_id, episode_id = self._create_project_and_episode(db)
        service = CharacterService(db)
        created = service.create(project_id, CharacterCreate(episode_id=episode_id, name="原始"))

        updated = service.update(created.id, CharacterUpdate(name="新名称", description="新描述"))

        assert updated.name == "新名称"
        assert updated.description == "新描述"

    def test_delete_character(self, db: Session):
        """Test deleting a character via service."""
        project_id, episode_id = self._create_project_and_episode(db)
        service = CharacterService(db)
        created = service.create(project_id, CharacterCreate(episode_id=episode_id, name="待删除"))

        result = service.delete(created.id)

        assert result is True
        assert service.get(created.id) is None

    def test_update_avatar(self, db: Session):
        """Test updating character avatar."""
        project_id, episode_id = self._create_project_and_episode(db)
        service = CharacterService(db)
        created = service.create(project_id, CharacterCreate(episode_id=episode_id, name="主角"))

        updated = service.update_avatar(created.id, "http://example.com/avatar.jpg")

        assert updated.avatar == "http://example.com/avatar.jpg"
