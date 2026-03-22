from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.project import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project model."""

    def __init__(self, db: Session):
        super().__init__(Project, db)

    def get_by_name(self, name: str) -> Optional[Project]:
        """Get project by name."""
        return self.db.query(Project).filter(
            Project.name == name,
            Project.is_deleted == 0
        ).first()

    def search(
        self,
        keyword: Optional[str] = None,
        status: Optional[int] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[List[Project], int]:
        """Search projects with filters."""
        query = self.db.query(Project).filter(Project.is_deleted == 0)

        if keyword:
            query = query.filter(
                or_(
                    Project.name.ilike(f"%{keyword}%"),
                    Project.description.ilike(f"%{keyword}%")
                )
            )

        if status is not None:
            query = query.filter(Project.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(Project.created_at.desc()).offset(offset).limit(page_size).all()

        return items, total

    def update_progress(self, id: int, progress: int) -> Optional[Project]:
        """Update project progress."""
        return self.update(id, progress=progress)

    def increment_chapter_count(self, id: int) -> Optional[Project]:
        """Increment project chapter count."""
        project = self.get(id)
        if project:
            project.chapter_count = (project.chapter_count or 0) + 1
            self.db.commit()
            self.db.refresh(project)
        return project

    def decrement_chapter_count(self, id: int) -> Optional[Project]:
        """Decrement project chapter count."""
        project = self.get(id)
        if project and project.chapter_count > 0:
            project.chapter_count = project.chapter_count - 1
            self.db.commit()
            self.db.refresh(project)
        return project
