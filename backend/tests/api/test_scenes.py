import pytest
from fastapi.testclient import TestClient


class TestSceneAPI:
    """Tests for scene API endpoints."""

    def _create_project_and_episode(self, client: TestClient) -> tuple:
        """Helper to create project and episode."""
        proj_response = client.post("/api/v1/projects", json={"name": "测试项目"})
        project_id = proj_response.json()["data"]["id"]

        ep_response = client.post(
            f"/api/v1/projects/{project_id}/episodes",
            json={"name": "第一章", "chapter_number": 1}
        )
        episode_id = ep_response.json()["data"]["id"]

        return project_id, episode_id

    def test_create_scene(self, client: TestClient):
        """Test creating a new scene."""
        project_id, episode_id = self._create_project_and_episode(client)

        response = client.post(
            f"/api/v1/projects/{project_id}/scenes",
            json={"name": "室内场景", "description": "客厅", "episode_id": episode_id}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == "室内场景"
        assert data["data"]["description"] == "客厅"

    def test_list_scenes(self, client: TestClient):
        """Test listing scenes for a project."""
        project_id, episode_id = self._create_project_and_episode(client)

        # Create scenes
        client.post(
            f"/api/v1/projects/{project_id}/scenes",
            json={"name": "场景1", "description": "描述1", "episode_id": episode_id}
        )
        client.post(
            f"/api/v1/projects/{project_id}/scenes",
            json={"name": "场景2", "description": "描述2", "episode_id": episode_id}
        )

        response = client.get(f"/api/v1/projects/{project_id}/scenes")
        assert response.status_code == 200
        assert response.json()["data"]["total"] == 2

    def test_get_scene(self, client: TestClient):
        """Test getting a scene by ID."""
        project_id, episode_id = self._create_project_and_episode(client)

        create_response = client.post(
            f"/api/v1/projects/{project_id}/scenes",
            json={"name": "场景", "description": "描述", "episode_id": episode_id}
        )
        scene_id = create_response.json()["data"]["id"]

        response = client.get(f"/api/v1/scenes/{scene_id}")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == scene_id

    def test_update_scene(self, client: TestClient):
        """Test updating a scene."""
        project_id, episode_id = self._create_project_and_episode(client)

        create_response = client.post(
            f"/api/v1/projects/{project_id}/scenes",
            json={"name": "场景", "description": "描述", "episode_id": episode_id}
        )
        scene_id = create_response.json()["data"]["id"]

        response = client.put(
            f"/api/v1/scenes/{scene_id}",
            json={"name": "新场景名称", "thumbnail": "http://example.com/thumb.jpg"}
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["name"] == "新场景名称"
        assert data["thumbnail"] == "http://example.com/thumb.jpg"

    def test_delete_scene(self, client: TestClient):
        """Test deleting a scene."""
        project_id, episode_id = self._create_project_and_episode(client)

        create_response = client.post(
            f"/api/v1/projects/{project_id}/scenes",
            json={"name": "场景", "description": "描述", "episode_id": episode_id}
        )
        scene_id = create_response.json()["data"]["id"]

        response = client.delete(f"/api/v1/scenes/{scene_id}")
        assert response.status_code == 200

        # Verify it's gone
        get_response = client.get(f"/api/v1/scenes/{scene_id}")
        assert get_response.status_code == 404
