import pytest
from fastapi.testclient import TestClient


class TestProjectAPI:
    """Tests for project API endpoints."""

    def test_create_project(self, client: TestClient, sample_project_data):
        """Test creating a new project."""
        response = client.post("/api/v1/projects", json=sample_project_data)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["name"] == sample_project_data["name"]
        assert data["data"]["description"] == sample_project_data["description"]
        assert "id" in data["data"]

    def test_create_project_without_name(self, client: TestClient):
        """Test creating project without name fails."""
        response = client.post("/api/v1/projects", json={"description": "test"})
        assert response.status_code == 422  # Validation error

    def test_list_projects_empty(self, client: TestClient):
        """Test listing projects when none exist."""
        response = client.get("/api/v1/projects")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["items"] == []
        assert data["data"]["total"] == 0

    def test_list_projects_with_data(self, client: TestClient, sample_project_data):
        """Test listing projects with existing data."""
        # Create a project first
        client.post("/api/v1/projects", json=sample_project_data)

        # List projects
        response = client.get("/api/v1/projects")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 1
        assert len(data["data"]["items"]) == 1

    def test_get_project(self, client: TestClient, sample_project_data):
        """Test getting a project by ID."""
        # Create a project
        create_response = client.post("/api/v1/projects", json=sample_project_data)
        project_id = create_response.json()["data"]["id"]

        # Get the project
        response = client.get(f"/api/v1/projects/{project_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == project_id
        assert data["data"]["name"] == sample_project_data["name"]

    def test_get_project_not_found(self, client: TestClient):
        """Test getting non-existent project."""
        response = client.get("/api/v1/projects/99999")
        assert response.status_code == 404

    def test_update_project(self, client: TestClient, sample_project_data):
        """Test updating a project."""
        # Create a project
        create_response = client.post("/api/v1/projects", json=sample_project_data)
        project_id = create_response.json()["data"]["id"]

        # Update the project
        update_data = {"name": "更新的名称"}
        response = client.put(f"/api/v1/projects/{project_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == "更新的名称"
        assert data["data"]["description"] == sample_project_data["description"]  # Unchanged

    def test_delete_project(self, client: TestClient, sample_project_data):
        """Test deleting a project."""
        # Create a project
        create_response = client.post("/api/v1/projects", json=sample_project_data)
        project_id = create_response.json()["data"]["id"]

        # Delete the project
        response = client.delete(f"/api/v1/projects/{project_id}")
        assert response.status_code == 200
        assert response.json()["data"]["deleted"] is True

        # Verify it's gone
        get_response = client.get(f"/api/v1/projects/{project_id}")
        assert get_response.status_code == 404

    def test_search_projects_by_keyword(self, client: TestClient):
        """Test searching projects by keyword."""
        # Create projects
        client.post("/api/v1/projects", json={"name": "项目A", "description": "描述A"})
        client.post("/api/v1/projects", json={"name": "项目B", "description": "描述B"})

        # Search
        response = client.get("/api/v1/projects?keyword=项目A")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 1
        assert data["data"]["items"][0]["name"] == "项目A"

    def test_filter_projects_by_status(self, client: TestClient):
        """Test filtering projects by status."""
        # Create projects with different statuses
        client.post("/api/v1/projects", json={"name": "草稿项目", "status": 0})
        client.post("/api/v1/projects", json={"name": "进行中项目", "status": 1})

        # Filter by status
        response = client.get("/api/v1/projects?status=1")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 1
        assert data["data"]["items"][0]["status"] == 1

    def test_pagination(self, client: TestClient):
        """Test project pagination."""
        # Create 15 projects
        for i in range(15):
            client.post("/api/v1/projects", json={"name": f"项目{i}"})

        # Get first page
        response = client.get("/api/v1/projects?page=1&page_size=10")
        data = response.json()
        assert data["data"]["total"] == 15
        assert len(data["data"]["items"]) == 10
        assert data["data"]["page"] == 1
        assert data["data"]["page_size"] == 10

        # Get second page
        response = client.get("/api/v1/projects?page=2&page_size=10")
        data = response.json()
        assert len(data["data"]["items"]) == 5
