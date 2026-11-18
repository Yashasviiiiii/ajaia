"""Tests for file import functionality."""
import io
import pytest
from fastapi.testclient import TestClient

from tests.conftest import auth_headers


def test_import_txt_file(client: TestClient, alice_token: str):
    """Test importing a plain text file."""
    content = "This is a test.\n\nSecond paragraph."
    
    response = client.post(
        "/api/documents/import",
        files={"file": ("test.txt", io.BytesIO(content.encode("utf-8")), "text/plain")},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "test.txt"
    assert data["file_extension"] == ".txt"
    assert "<p>This is a test.</p>" in data["content"]
    assert "<p>Second paragraph.</p>" in data["content"]


def test_import_md_file(client: TestClient, alice_token: str):
    """Test importing a markdown file."""
    content = "# Heading\n\nThis is **bold** and *italic*."
    
    response = client.post(
        "/api/documents/import",
        files={"file": ("test.md", io.BytesIO(content.encode("utf-8")), "text/markdown")},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "test.md"
    assert data["file_extension"] == ".md"
    assert "<h1>Heading</h1>" in data["content"]
    assert "<strong>bold</strong>" in data["content"]
    assert "<em>italic</em>" in data["content"]


def test_import_md_strips_tables(client: TestClient, alice_token: str):
    """Test that markdown tables are stripped on import."""
    content = """# Document

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

Normal paragraph."""
    
    response = client.post(
        "/api/documents/import",
        files={"file": ("test.md", io.BytesIO(content.encode("utf-8")), "text/markdown")},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 201
    data = response.json()
    # Tables should be stripped
    assert "<table>" not in data["content"]
    assert "<td>" not in data["content"]
    # Other content should remain
    assert "<h1>Document</h1>" in data["content"]
    assert "<p>Normal paragraph.</p>" in data["content"]


def test_import_duplicate_filename_auto_rename(client: TestClient, alice_token: str):
    """Test that duplicate imported files are auto-renamed."""
    content = "First import"
    
    # First import
    response1 = client.post(
        "/api/documents/import",
        files={"file": ("test.txt", io.BytesIO(content.encode("utf-8")), "text/plain")},
        headers=auth_headers(alice_token)
    )
    assert response1.status_code == 201
    assert response1.json()["title"] == "test.txt"
    
    # Second import with same filename
    content2 = "Second import"
    response2 = client.post(
        "/api/documents/import",
        files={"file": ("test.txt", io.BytesIO(content2.encode("utf-8")), "text/plain")},
        headers=auth_headers(alice_token)
    )
    assert response2.status_code == 201
    assert response2.json()["title"] == "test.txt (2)"


def test_import_unsupported_extension(client: TestClient, alice_token: str):
    """Test that unsupported file types are rejected."""
    response = client.post(
        "/api/documents/import",
        files={"file": ("test.pdf", io.BytesIO(b"fake pdf"), "application/pdf")},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 415
    assert "Unsupported" in response.json()["detail"]


def test_import_file_too_large(client: TestClient, alice_token: str):
    """Test that files over 5MB are rejected."""
    # Create a 6MB file
    large_content = b"x" * (6 * 1024 * 1024)
    
    response = client.post(
        "/api/documents/import",
        files={"file": ("large.txt", io.BytesIO(large_content), "text/plain")},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 413
    assert "too large" in response.json()["detail"].lower()


def test_import_empty_file(client: TestClient, alice_token: str):
    """Test that empty files are rejected."""
    response = client.post(
        "/api/documents/import",
        files={"file": ("empty.txt", io.BytesIO(b""), "text/plain")},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_import_non_utf8_text(client: TestClient, alice_token: str):
    """Test that non-UTF-8 text files are rejected."""
    # Create invalid UTF-8 bytes
    invalid_utf8 = b"\xff\xfe Invalid UTF-8"
    
    response = client.post(
        "/api/documents/import",
        files={"file": ("test.txt", io.BytesIO(invalid_utf8), "text/plain")},
        headers=auth_headers(alice_token)
    )
    
    assert response.status_code == 422
    assert "UTF-8" in response.json()["detail"]


def test_import_preserves_file_extension(client: TestClient, alice_token: str):
    """Test that imported files maintain their extension in the title."""
    files = [
        ("notes.txt", ".txt"),
        ("doc.md", ".md"),
        ("report.docx", ".docx"),
    ]
    
    for filename, expected_ext in files:
        content = b"Test content"
        response = client.post(
            "/api/documents/import",
            files={"file": (filename, io.BytesIO(content), "text/plain")},
            headers=auth_headers(alice_token)
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["file_extension"] == expected_ext
        assert data["title"].endswith(expected_ext)
