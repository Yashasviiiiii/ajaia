"""Tests for document CRUD operations."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User
from tests.conftest import auth_headers


def test_create_document_default(client: TestClient, alice_token: str):
    """Test creating a document with default values."""
    response = client.post(
        "/api/documents",
        json={},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Untitled document"
    assert data["content"] == "<p></p>"
    assert data["file_extension"] is None
    assert data["role"] == "owner"


def test_create_document_with_title(client: TestClient, alice_token: str):
    """Test creating a document with custom title."""
    response = client.post(
        "/api/documents",
        json={"title": "My Document", "content": "<p>Hello</p>"},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Document"
    assert data["content"] == "<p>Hello</p>"


def test_create_document_with_extension(client: TestClient, alice_token: str):
    """Test creating a document with file extension."""
    response = client.post(
        "/api/documents",
        json={"title": "Notes", "file_extension": ".md"},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Notes.md"
    assert data["file_extension"] == ".md"


def test_create_duplicate_documents_auto_rename(client: TestClient, alice_token: str):
    """Test that duplicate document names are auto-renamed."""
    # Create first document
    response1 = client.post(
        "/api/documents",
        json={"title": "Test.md", "file_extension": ".md"},
        headers=auth_headers(alice_token)
    )
    assert response1.status_code == 201
    assert response1.json()["title"] == "Test.md"
    
    # Create second document with same name
    response2 = client.post(
        "/api/documents",
        json={"title": "Test.md", "file_extension": ".md"},
        headers=auth_headers(alice_token)
    )
    assert response2.status_code == 201
    assert response2.json()["title"] == "Test.md (2)"
    
    # Create third document
    response3 = client.post(
        "/api/documents",
        json={"title": "Test.md", "file_extension": ".md"},
        headers=auth_headers(alice_token)
    )
    assert response3.status_code == 201
    assert response3.json()["title"] == "Test.md (3)"


def test_list_documents_empty(client: TestClient, alice_token: str):
    """Test listing documents when none exist."""
    response = client.get("/api/documents", headers=auth_headers(alice_token))
    
    assert response.status_code == 200
    data = response.json()
    assert data["owned"] == []
    assert data["shared"] == []


def test_list_documents_owned(client: TestClient, alice_token: str):
    """Test listing owned documents."""
    # Create a document
    client.post(
        "/api/documents",
        json={"title": "Alice's Doc"},
        headers=auth_headers(alice_token)
    )
    
    response = client.get("/api/documents", headers=auth_headers(alice_token))
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["owned"]) == 1
    assert data["owned"][0]["title"] == "Alice's Doc"
    assert data["owned"][0]["role"] == "owner"


def test_get_document(client: TestClient, alice_token: str):
    """Test getting a specific document."""
    # Create document
    create_response = client.post(
        "/api/documents",
        json={"title": "Test Doc", "content": "<p>Content</p>"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    # Get document
    response = client.get(
        f"/api/documents/{doc_id}",
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Doc"
    assert data["content"] == "<p>Content</p>"


def test_get_nonexistent_document(client: TestClient, alice_token: str):
    """Test getting a document that doesn't exist."""
    response = client.get(
        "/api/documents/9999",
        headers=auth_headers(alice_token)
    )
    assert response.status_code == 404


def test_update_document_title(client: TestClient, alice_token: str):
    """Test updating document title."""
    # Create document
    create_response = client.post(
        "/api/documents",
        json={"title": "Old Title"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    # Update title
    response = client.patch(
        f"/api/documents/{doc_id}",
        json={"title": "New Title"},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


def test_update_document_content(client: TestClient, alice_token: str):
    """Test updating document content."""
    # Create document
    create_response = client.post(
        "/api/documents",
        json={"content": "<p>Old</p>"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    # Update content
    response = client.patch(
        f"/api/documents/{doc_id}",
        json={"content": "<p>New content</p>"},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 200
    assert response.json()["content"] == "<p>New content</p>"


def test_update_document_duplicate_title_fails(client: TestClient, alice_token: str):
    """Test that renaming to existing title fails."""
    # Create two documents
    client.post(
        "/api/documents",
        json={"title": "Doc 1"},
        headers=auth_headers(alice_token)
    )
    response2 = client.post(
        "/api/documents",
        json={"title": "Doc 2"},
        headers=auth_headers(alice_token)
    )
    doc2_id = response2.json()["id"]
    
    # Try to rename Doc 2 to Doc 1
    response = client.patch(
        f"/api/documents/{doc2_id}",
        json={"title": "Doc 1"},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 400
    assert "already have a document named" in response.json()["detail"]


def test_delete_document(client: TestClient, alice_token: str):
    """Test deleting a document."""
    # Create document
    create_response = client.post(
        "/api/documents",
        json={"title": "To Delete"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(
        f"/api/documents/{doc_id}",
        headers=auth_headers(alice_token)
    )
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(
        f"/api/documents/{doc_id}",
        headers=auth_headers(alice_token)
    )
    assert get_response.status_code == 404


def test_html_sanitization(client: TestClient, alice_token: str):
    """Test that HTML is sanitized on create/update."""
    # Try to create document with script tag
    response = client.post(
        "/api/documents",
        json={"content": "<p>Safe</p><script>alert('xss')</script>"},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "<script>" not in data["content"]
    assert "alert" not in data["content"]
    assert "<p>Safe</p>" in data["content"]
