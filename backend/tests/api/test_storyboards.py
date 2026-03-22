import pytest
from fastapi.testclient import TestClient


class TestStoryboardAPI:
    """Tests for storyboard API endpoints."""

    def _create_project_and_episode(self, client: TestClient):
        """Helper to create project and episode, return IDs."""
        project_resp = client.post("/api/v1/projects", json={"name": "测试项目"})
        project_id = project_resp.json()["data"]["id"]
        episode_resp = client.post(
            f"/api/v1/episodes/projects/{project_id}/episodes",
            json={"name": "第一章", "content": "测试内容", "chapter_number": 1}
        )
        episode_id = episode_resp.json()["data"]["id"]
        return project_id, episode_id

    def test_create_storyboard(self, client: TestClient):
        """Test creating a new storyboard."""
        project_id, episode_id = self._create_project_and_episode(client)

        response = client.post(
            f"/api/v1/storyboards/episodes/{episode_id}/storyboards",
            json={
                "episode_id": episode_id,
                "shot_number": 1,
                "shot_type": 1,
                "duration": 5,
                "description": "测试镜头"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["description"] == "测试镜头"

    def test_list_storyboards(self, client: TestClient):
        """Test listing storyboards for an episode."""
        project_id, episode_id = self._create_project_and_episode(client)

        # Create storyboards
        for i in range(3):
            client.post(
                f"/api/v1/storyboards/episodes/{episode_id}/storyboards",
                json={"episode_id": episode_id, "shot_number": i+1, "shot_type": 1, "duration": 5, "description": f"镜头{i}"}
            )

        response = client.get(f"/api/v1/storyboards/episodes/{episode_id}/storyboards")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 3

    def test_get_storyboard(self, client: TestClient):
        """Test getting a storyboard by ID."""
        project_id, episode_id = self._create_project_and_episode(client)

        create_resp = client.post(
            f"/api/v1/storyboards/episodes/{episode_id}/storyboards",
            json={"episode_id": episode_id, "shot_number": 1, "shot_type": 1, "duration": 5, "description": "测试"}
        )
        storyboard_id = create_resp.json()["data"]["id"]

        response = client.get(f"/api/v1/storyboards/{storyboard_id}")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == storyboard_id

    def test_update_storyboard(self, client: TestClient):
        """Test updating a storyboard."""
        project_id, episode_id = self._create_project_and_episode(client)

        create_resp = client.post(
            f"/api/v1/storyboards/episodes/{episode_id}/storyboards",
            json={"episode_id": episode_id, "shot_number": 1, "shot_type": 1, "duration": 5, "description": "原始"}
        )
        storyboard_id = create_resp.json()["data"]["id"]

        response = client.put(
            f"/api/v1/storyboards/{storyboard_id}",
            json={"description": "更新后"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["description"] == "更新后"

    def test_delete_storyboard(self, client: TestClient):
        """Test deleting a storyboard."""
        project_id, episode_id = self._create_project_and_episode(client)

        create_resp = client.post(
            f"/api/v1/storyboards/episodes/{episode_id}/storyboards",
            json={"episode_id": episode_id, "shot_number": 1, "shot_type": 1, "duration": 5, "description": "待删除"}
        )
        storyboard_id = create_resp.json()["data"]["id"]

        response = client.delete(f"/api/v1/storyboards/{storyboard_id}")
        assert response.status_code == 200

        # Verify deleted
        get_resp = client.get(f"/api/v1/storyboards/{storyboard_id}")
        assert get_resp.status_code == 404