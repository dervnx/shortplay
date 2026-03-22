import pytest
from sqlalchemy.orm import Session

from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate


class TestProjectService:
    """Tests for ProjectService."""

    def test_create_project(self, db: Session):
        """Test creating a project via service."""
        service = ProjectService(db)
        schema = ProjectCreate(name="测试项目", description="测试描述")

        project = service.create(schema)

        assert project.id is not None
        assert project.name == "测试项目"
        assert project.description == "测试描述"
        assert project.status == 0
        assert project.progress == 0

    def test_get_project(self, db: Session):
        """Test getting a project via service."""
        service = ProjectService(db)
        schema = ProjectCreate(name="测试项目")

        created = service.create(schema)
        retrieved = service.get(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == "测试项目"

    def test_get_nonexistent_project(self, db: Session):
        """Test getting non-existent project returns None."""
        service = ProjectService(db)
        result = service.get(99999)
        assert result is None

    def test_list_projects(self, db: Session):
        """Test listing projects with pagination."""
        service = ProjectService(db)

        # Create 5 projects
        for i in range(5):
            service.create(ProjectCreate(name=f"项目{i}"))

        result = service.list(page=1, page_size=3)

        assert result.total == 5
        assert len(result.items) == 3
        assert result.page == 1
        assert result.page_size == 3

    def test_search_projects(self, db: Session):
        """Test searching projects by keyword."""
        service = ProjectService(db)

        service.create(ProjectCreate(name="项目A", description="包含关键词"))
        service.create(ProjectCreate(name="项目B", description="不包含"))

        result = service.list(keyword="关键词")

        assert result.total == 1
        assert result.items[0].name == "项目A"

    def test_update_project(self, db: Session):
        """Test updating a project via service."""
        service = ProjectService(db)
        created = service.create(ProjectCreate(name="原始名称"))

        updated = service.update(created.id, ProjectUpdate(name="新名称"))

        assert updated is not None
        assert updated.name == "新名称"

    def test_delete_project(self, db: Session):
        """Test deleting a project via service."""
        service = ProjectService(db)
        created = service.create(ProjectCreate(name="待删除"))

        result = service.delete(created.id)

        assert result is True
        assert service.get(created.id) is None

    def test_update_progress(self, db: Session):
        """Test updating project progress."""
        service = ProjectService(db)
        created = service.create(ProjectCreate(name="测试"))

        updated = service.update_progress(created.id, 50)

        assert updated.progress == 50
        assert updated.status == 1  # 处理中

    def test_update_progress_to_complete(self, db: Session):
        """Test updating project progress to 100."""
        service = ProjectService(db)
        created = service.create(ProjectCreate(name="测试"))

        updated = service.update_progress(created.id, 100)

        assert updated.progress == 100
        assert updated.status == 2  # 已完成
