"""
Integration tests for the Personal Blog API

These tests verify the complete workflow of the application,
testing multiple components working together.
"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_user_registration_and_login():
    """Test complete user registration and login flow"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Register new user
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = await client.post("/api/v1/auth/register", json=register_data)
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 200
        assert "token" in data["data"]

        # Login with credentials
        login_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "token" in data["data"]

        token = data["data"]["token"]

        # Get current user info
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["username"] == "testuser"


@pytest.mark.asyncio
async def test_article_crud_workflow():
    """Test complete article CRUD workflow"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Login as admin (assuming admin exists)
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        token = response.json()["data"]["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create article
        article_data = {
            "title": "Test Article",
            "content": "# Test Content\n\nThis is a test article.",
            "summary": "Test summary",
            "board": "tech",
            "tags": ["test", "integration"],
            "is_published": True
        }
        response = await client.post(
            "/api/v1/articles",
            json=article_data,
            headers=headers
        )
        assert response.status_code == 201
        article_id = response.json()["data"]["id"]

        # Get article
        response = await client.get(f"/api/v1/articles/{article_id}")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["title"] == "Test Article"

        # Update article
        update_data = {"title": "Updated Test Article"}
        response = await client.put(
            f"/api/v1/articles/{article_id}",
            json=update_data,
            headers=headers
        )
        assert response.status_code == 200

        # Delete article
        response = await client.delete(
            f"/api/v1/articles/{article_id}",
            headers=headers
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_like_workflow():
    """Test article like workflow"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Assume article exists
        article_id = "test-article-id"

        # Toggle like (first time - like)
        response = await client.post(f"/api/v1/likes/{article_id}")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["action"] == "liked"

        # Check like status
        response = await client.get(f"/api/v1/likes/{article_id}/status")
        assert response.status_code == 200
        assert response.json()["data"]["is_liked"] is True

        # Toggle like (second time - unlike)
        response = await client.post(f"/api/v1/likes/{article_id}")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["action"] == "unliked"


@pytest.mark.asyncio
async def test_search_workflow():
    """Test search functionality"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Search articles
        response = await client.get("/api/v1/search/articles?q=test")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data

        # Global search
        response = await client.get("/api/v1/search/global?q=python")
        assert response.status_code == 200
        data = response.json()["data"]
        assert "articles" in data
        assert "skills" in data
        assert "projects" in data

        # Get suggestions
        response = await client.get("/api/v1/search/suggestions?q=test")
        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)


@pytest.mark.asyncio
async def test_statistics_endpoints():
    """Test statistics endpoints"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Overview stats
        response = await client.get("/api/v1/statistics/overview")
        assert response.status_code == 200
        data = response.json()["data"]
        assert "articles" in data
        assert "engagement" in data
        assert "portfolio" in data

        # Popular articles
        response = await client.get("/api/v1/statistics/articles/popular")
        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)

        # Tag stats
        response = await client.get("/api/v1/statistics/tags")
        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)


@pytest.mark.asyncio
async def test_skill_and_project_workflow():
    """Test skills and projects workflow"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Get skills grouped
        response = await client.get("/api/v1/skills/grouped")
        assert response.status_code == 200
        data = response.json()["data"]
        assert isinstance(data, dict)

        # Get projects
        response = await client.get("/api/v1/projects")
        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)

        # Get featured projects
        response = await client.get("/api/v1/projects/featured")
        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # 404 - Not found
        response = await client.get("/api/v1/articles/nonexistent-id")
        assert response.status_code == 404

        # 401 - Unauthorized
        response = await client.post("/api/v1/articles", json={})
        assert response.status_code == 401

        # 400 - Bad request
        response = await client.post("/api/v1/auth/register", json={})
        assert response.status_code == 422  # Validation error
