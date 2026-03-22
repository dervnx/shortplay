import pytest
from fastapi.testclient import TestClient


class TestCharacterAPI:
    """Tests for character API endpoints."""

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

    def test_create_character(self, client: TestClient, sample_character_data):
        """Test creating a new character."""
        project_id, episode_id = self._create_project_and_episode(client)

        response = client.post(
            f"/api/v1/projects/{project_id}/characters",
            json={**sample_character_data, "episode_id": episode_id}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == sample_character_data["name"]
        assert data["data"]["description"] == sample_character_data["description"]

    def test_list_characters(self, client: TestClient, sample_character_data):
        """Test listing characters for a project."""
        project_id, episode_id = self._create_project_and_episode(client)

        # Create characters
        client.post(
            f"/api/v1/projects/{project_id}/characters",
            json={**sample_character_data, "episode_id": episode_id, "name": "角色1"}
        )
        client.post(
            f"/api/v1/projects/{project_id}/characters",
            json={**sample_character_data, "episode_id": episode_id, "name": "角色2"}
        )

        response = client.get(f"/api/v1/projects/{project_id}/characters")
        assert response.status_code == 200
        assert response.json()["data"]["total"] == 2

    def test_get_character(self, client: TestClient, sample_character_data):
        """Test getting a character by ID."""
        project_id, episode_id = self._create_project_and_episode(client)

        create_response = client.post(
            f"/api/v1/projects/{project_id}/characters",
            json={**sample_character_data, "episode_id": episode_id}
        )
        character_id = create_response.json()["data"]["id"]

        response = client.get(f"/api/v1/characters/{character_id}")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == character_id

    def test_update_character(self, client: TestClient, sample_character_data):
        """Test updating a character."""
        project_id, episode_id = self._create_project_and_episode(client)

        create_response = client.post(
            f"/api/v1/projects/{project_id}/characters",
            json={**sample_character_data, "episode_id": episode_id}
        )
        character_id = create_response.json()["data"]["id"]

        response = client.put(
            f"/api/v1/characters/{character_id}",
            json={"name": "新名称", "description": "新描述"}
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["name"] == "新名称"
        assert data["description"] == "新描述"

    def test_delete_character(self, client: TestClient, sample_character_data):
        """Test deleting a character."""
        project_id, episode_id = self._create_project_and_episode(client)

        create_response = client.post(
            f"/api/v1/projects/{project_id}/characters",
            json={**sample_character_data, "episode_id": episode_id}
        )
        character_id = create_response.json()["data"]["id"]

        response = client.delete(f"/api/v1/characters/{character_id}")
        assert response.status_code == 200

        # Verify it's gone
        get_response = client.get(f"/api/v1/characters/{character_id}")
        assert get_response.status_code == 404

    def test_search_characters(self, client: TestClient, sample_character_data):
        """Test searching characters by keyword."""
        project_id, episode_id = self._create_project_and_episode(client)

        client.post(
            f"/api/v1/projects/{project_id}/characters",
            json={**sample_character_data, "episode_id": episode_id, "name": "张三"}
        )
        client.post(
            f"/api/v1/projects/{project_id}/characters",
            json={**sample_character_data, "episode_id": episode_id, "name": "李四"}
        )

        response = client.get(f"/api/v1/projects/{project_id}/characters?keyword=张三")
        assert response.status_code == 200
        assert response.json()["data"]["total"] == 1
        assert response.json()["data"]["items"][0]["name"] == "张三"
