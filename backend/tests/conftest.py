import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import get_db
from app.models.base import BaseModel as Base  # Use BaseModel which has models registered
from app.models import *  # noqa: F401, F403 - Import models to register them with Base
from app.core.config import settings

# Use the same DATABASE_URL as the app (supports PostgreSQL with JSONB)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        "name": "测试短剧",
        "description": "这是一个测试项目",
    }


@pytest.fixture
def sample_episode_data():
    """Sample episode data for testing."""
    return {
        "name": "第一章",
        "content": "故事内容...",
        "chapter_number": 1,
    }


@pytest.fixture
def sample_character_data():
    """Sample character data for testing."""
    return {
        "name": "主角",
        "description": "故事的主角",
    }


@pytest.fixture
def sample_script():
    """Sample script text for AI testing."""
    return """
    第一幕：咖啡馆内，日，内
    主角李明走进咖啡馆，看到他的老朋友王芳坐在角落。

    李明：（惊讶）王芳？好久不见！
    王芳：（微笑）李明！真巧，我刚到。

    场景转换：咖啡馆外，日，外
    李明和王芳走在街上，讨论着过去的事情。
    """
