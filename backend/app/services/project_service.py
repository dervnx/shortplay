from __future__ import annotations
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.common import PaginatedResponse
from app.repositories.project import ProjectRepository


class ProjectService:
    """Service for project business logic."""

    def __init__(self, db: Session):
        self.repo = ProjectRepository(db)

    def create(self, schema: ProjectCreate) -> Project:
        """Create a new project."""
        return self.repo.create(
            name=schema.name,
            description=schema.description,
            cover=schema.cover,
            style_id=schema.style_id,
            status=schema.status if schema.status is not None else 0,
            progress=0,
        )

    def get(self, id: int) -> Optional[Project]:
        """Get project by ID."""
        return self.repo.get(id)

    def list(
        self,
        keyword: Optional[str] = None,
        status: Optional[int] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedResponse[Project]:
        """List projects with pagination and filters."""
        items, total = self.repo.search(
            keyword=keyword,
            status=status,
            page=page,
            page_size=page_size,
        )
        return PaginatedResponse.create(items, total, page, page_size)

    def update(self, id: int, schema: ProjectUpdate) -> Optional[Project]:
        """Update a project."""
        update_data = schema.model_dump(exclude_unset=True)
        return self.repo.update(id, **update_data)

    def delete(self, id: int) -> bool:
        """Delete a project."""
        return self.repo.delete(id)

    def update_progress(self, id: int, progress: int) -> Optional[Project]:
        """Update project progress."""
        project = self.repo.get(id)
        if project:
            project.progress = progress
            if progress >= 100:
                project.status = 2  # 已完成
            elif progress > 0:
                project.status = 1  # 处理中
            self.repo.db.commit()
            self.repo.db.refresh(project)
        return project
