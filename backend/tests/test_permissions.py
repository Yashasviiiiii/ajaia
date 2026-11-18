"""Tests for document sharing and access control."""
import pytest
from fastapi.testclient import TestClient

from tests.conftest import auth_headers


def test_share_document_view_permission(client: TestClient, alice_token: str, bob_token: str):
    """Test sharing a document with view permission."""
    # Alice creates a document
    create_response = client.post(
        "/api/documents",
        json={"title": "Shared Doc"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    # Alice shares with Bob (view)
    response = client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "bob@test.com", "permission": "view"},
        headers=auth_headers(alice_token)
    )
    assert response.status_code == 201
    
    # Bob can see it in shared list
    list_response = client.get("/api/documents", headers=auth_headers(bob_token))
    assert len(list_response.json()["shared"]) == 1
    assert list_response.json()["shared"][0]["role"] == "view"
    
    # Bob can read it
    get_response = client.get(
        f"/api/documents/{doc_id}",
        headers=auth_headers(bob_token)
    )
    assert get_response.status_code == 200
    assert get_response.json()["role"] == "view"


def test_share_document_edit_permission(client: TestClient, alice_token: str, bob_token: str):
    """Test sharing a document with edit permission."""
    # Alice creates a document
    create_response = client.post(
        "/api/documents",
        json={"title": "Editable Doc"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    # Alice shares with Bob (edit)
    client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "bob@test.com", "permission": "edit"},
        headers=auth_headers(alice_token)
    )
    
    # Bob can edit it
    update_response = client.patch(
        f"/api/documents/{doc_id}",
        json={"content": "<p>Bob's edit</p>"},
        headers=auth_headers(bob_token)
    )
    assert update_response.status_code == 200


def test_view_only_cannot_edit(client: TestClient, alice_token: str, bob_token: str):
    """Test that view-only users cannot edit."""
    # Alice creates and shares with view permission
    create_response = client.post(
        "/api/documents",
        json={"title": "View Only Doc"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "bob@test.com", "permission": "view"},
        headers=auth_headers(alice_token)
    )
    
    # Bob tries to edit
    response = client.patch(
        f"/api/documents/{doc_id}",
        json={"content": "<p>Trying to edit</p>"},
        headers=auth_headers(bob_token)
    )
    
    assert response.status_code == 403
    assert "view-only" in response.json()["detail"].lower()


def test_non_owner_cannot_delete(client: TestClient, alice_token: str, bob_token: str):
    """Test that non-owners cannot delete documents."""
    # Alice creates and shares with edit permission
    create_response = client.post(
        "/api/documents",
        json={"title": "Doc"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "bob@test.com", "permission": "edit"},
        headers=auth_headers(alice_token)
    )
    
    # Bob tries to delete
    response = client.delete(
        f"/api/documents/{doc_id}",
        headers=auth_headers(bob_token)
    )
    
    assert response.status_code == 403


def test_non_owner_cannot_share(client: TestClient, alice_token: str, bob_token: str, carol_token: str):
    """Test that non-owners cannot share documents."""
    # Alice creates and shares with Bob
    create_response = client.post(
        "/api/documents",
        json={"title": "Doc"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "bob@test.com", "permission": "edit"},
        headers=auth_headers(alice_token)
    )
    
    # Bob tries to share with Carol
    response = client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "carol@test.com", "permission": "view"},
        headers=auth_headers(bob_token)
    )
    
    assert response.status_code == 403


def test_unshared_document_returns_404(client: TestClient, alice_token: str, bob_token: str):
    """Test that unshared documents appear as 404 (not 403) to prevent existence leaking."""
    # Alice creates a document
    create_response = client.post(
        "/api/documents",
        json={"title": "Private Doc"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    # Bob tries to access it
    response = client.get(
        f"/api/documents/{doc_id}",
        headers=auth_headers(bob_token)
    )
    
    assert response.status_code == 404  # Not 403!


def test_update_share_permission(client: TestClient, alice_token: str, bob_token: str):
    """Test updating a share permission from view to edit."""
    # Alice creates and shares with view
    create_response = client.post(
        "/api/documents",
        json={"title": "Doc"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "bob@test.com", "permission": "view"},
        headers=auth_headers(alice_token)
    )
    
    # Verify Bob has view
    get_response = client.get(f"/api/documents/{doc_id}", headers=auth_headers(bob_token))
    assert get_response.json()["role"] == "view"
    
    # Alice upgrades to edit
    client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "bob@test.com", "permission": "edit"},
        headers=auth_headers(alice_token)
    )
    
    # Verify Bob now has edit
    get_response = client.get(f"/api/documents/{doc_id}", headers=auth_headers(bob_token))
    assert get_response.json()["role"] == "edit"


def test_revoke_share(client: TestClient, alice_token: str, bob_token: str, seed_users):
    """Test revoking a share."""
    # Alice creates and shares
    create_response = client.post(
        "/api/documents",
        json={"title": "Doc"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "bob@test.com", "permission": "view"},
        headers=auth_headers(alice_token)
    )
    
    # Bob can access
    assert client.get(f"/api/documents/{doc_id}", headers=auth_headers(bob_token)).status_code == 200
    
    # Alice revokes
    bob_id = seed_users["bob"].id
    revoke_response = client.delete(
        f"/api/documents/{doc_id}/shares/{bob_id}",
        headers=auth_headers(alice_token)
    )
    assert revoke_response.status_code == 204
    
    # Bob can no longer access
    assert client.get(f"/api/documents/{doc_id}", headers=auth_headers(bob_token)).status_code == 404


def test_list_shares(client: TestClient, alice_token: str):
    """Test listing shares for a document."""
    # Alice creates a document
    create_response = client.post(
        "/api/documents",
        json={"title": "Doc"},
        headers=auth_headers(alice_token)
    )
    doc_id = create_response.json()["id"]
    
    # Share with Bob and Carol
    client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "bob@test.com", "permission": "edit"},
        headers=auth_headers(alice_token)
    )
    client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "carol@test.com", "permission": "view"},
        headers=auth_headers(alice_token)
    )
    
    # List shares
    response = client.get(
        f"/api/documents/{doc_id}/shares",
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 200
    shares = response.json()
    assert len(shares) == 2
    
    emails = [s["user"]["email"] for s in shares]
    assert "bob@test.com" in emails
    assert "carol@test.com" in emails
