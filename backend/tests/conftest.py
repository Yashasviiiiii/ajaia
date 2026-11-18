"""Pytest fixtures and test configuration."""
import os
import tempfile
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import User
from app.security import hash_password


@pytest.fixture(scope="function")
def test_db() -> Generator[Session, None, None]:
    """Create a fresh test database for each test."""
    # Use in-memory SQLite for speed
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db: Session) -> TestClient:
    """Create a test client with test database."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def seed_users(test_db: Session) -> dict[str, User]:
    """Create test users."""
    users = {
        "alice": User(
            email="alice@test.com",
            name="Alice",
            password_hash=hash_password("password123")
        ),
        "bob": User(
            email="bob@test.com",
            name="Bob",
            password_hash=hash_password("password123")
        ),
        "carol": User(
            email="carol@test.com",
            name="Carol",
            password_hash=hash_password("password123")
        ),
    }
    
    for user in users.values():
        test_db.add(user)
    test_db.commit()
    
    for user in users.values():
        test_db.refresh(user)
    
    return users


@pytest.fixture(scope="function")
def alice_token(client: TestClient, seed_users: dict[str, User]) -> str:
    """Get auth token for Alice."""
    response = client.post("/api/auth/login", json={
        "email": "alice@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def bob_token(client: TestClient, seed_users: dict[str, User]) -> str:
    """Get auth token for Bob."""
    response = client.post("/api/auth/login", json={
        "email": "bob@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def carol_token(client: TestClient, seed_users: dict[str, User]) -> str:
    """Get auth token for Carol."""
    response = client.post("/api/auth/login", json={
        "email": "carol@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]


def auth_headers(token: str) -> dict[str, str]:
    """Helper to create authorization headers."""
    return {"Authorization": f"Bearer {token}"}
