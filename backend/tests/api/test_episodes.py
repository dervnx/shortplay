import pytest
from fastapi.testclient import TestClient


class TestEpisodeAPI:
    """Tests for episode API endpoints."""

    def _create_project(self, client: TestClient, name: str = "测试项目") -> int:
        """Helper to create a project and return its ID."""
        response = client.post("/api/v1/projects", json={"name": name})
        return response.json()["data"]["id"]

    def test_create_episode(self, client: TestClient, sample_episode_data):
        """Test creating a new episode."""
        project_id = self._create_project(client)

        response = client.post(
            f"/api/v1/projects/{project_id}/episodes",
            json=sample_episode_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == sample_episode_data["name"]
        assert data["data"]["chapter_number"] == sample_episode_data["chapter_number"]
        assert data["data"]["project_id"] == project_id

    def test_list_episodes(self, client: TestClient):
        """Test listing episodes for a project."""
        project_id = self._create_project(client)

        # Create episodes
        client.post(f"/api/v1/projects/{project_id}/episodes", json={"name": "第一章", "chapter_number": 1})
        client.post(f"/api/v1/projects/{project_id}/episodes", json={"name": "第二章", "chapter_number": 2})

        # List episodes
        response = client.get(f"/api/v1/projects/{project_id}/episodes")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 2
        assert len(data["data"]["items"]) == 2

    def test_get_episode(self, client: TestClient, sample_episode_data):
        """Test getting an episode by ID."""
        project_id = self._create_project(client)
        create_response = client.post(
            f"/api/v1/projects/{project_id}/episodes",
            json=sample_episode_data
        )
        episode_id = create_response.json()["data"]["id"]

        response = client.get(f"/api/v1/episodes/{episode_id}")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == episode_id

    def test_get_episode_not_found(self, client: TestClient):
        """Test getting non-existent episode."""
        response = client.get("/api/v1/episodes/99999")
        assert response.status_code == 404

    def test_update_episode(self, client: TestClient, sample_episode_data):
        """Test updating an episode."""
        project_id = self._create_project(client)
        create_response = client.post(
            f"/api/v1/projects/{project_id}/episodes",
            json=sample_episode_data
        )
        episode_id = create_response.json()["data"]["id"]

        response = client.put(
            f"/api/v1/episodes/{episode_id}",
            json={"name": "更新的章节名称"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "更新的章节名称"

    def test_delete_episode(self, client: TestClient, sample_episode_data):
        """Test deleting an episode."""
        project_id = self._create_project(client)
        create_response = client.post(
            f"/api/v1/projects/{project_id}/episodes",
            json=sample_episode_data
        )
        episode_id = create_response.json()["data"]["id"]

        response = client.delete(f"/api/v1/episodes/{episode_id}")
        assert response.status_code == 200

        # Verify it's gone
        get_response = client.get(f"/api/v1/episodes/{episode_id}")
        assert get_response.status_code == 404

    def test_episode_pagination(self, client: TestClient):
        """Test episode pagination."""
        project_id = self._create_project(client)

        # Create 12 episodes
        for i in range(12):
            client.post(
                f"/api/v1/projects/{project_id}/episodes",
                json={"name": f"章节{i}", "chapter_number": i + 1}
            )

        # Get first page
        response = client.get(f"/api/v1/projects/{project_id}/episodes?page=1&page_size=10")
        data = response.json()
        assert data["data"]["total"] == 12
        assert len(data["data"]["items"]) == 10
