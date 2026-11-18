"""Tests for authentication endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User


def test_login_success(client: TestClient, seed_users: dict[str, User]):
    """Test successful login."""
    response = client.post("/api/auth/login", json={
        "email": "alice@test.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "alice@test.com"
    assert data["user"]["name"] == "Alice"


def test_login_invalid_email(client: TestClient, seed_users: dict[str, User]):
    """Test login with non-existent email."""
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@test.com",
        "password": "password123"
    })
    
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_login_invalid_password(client: TestClient, seed_users: dict[str, User]):
    """Test login with wrong password."""
    response = client.post("/api/auth/login", json={
        "email": "alice@test.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_me_endpoint(client: TestClient, alice_token: str):
    """Test /auth/me endpoint."""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {alice_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice@test.com"
    assert data["name"] == "Alice"


def test_me_endpoint_no_token(client: TestClient):
    """Test /auth/me without token returns 401."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_me_endpoint_invalid_token(client: TestClient):
    """Test /auth/me with invalid token returns 401."""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
