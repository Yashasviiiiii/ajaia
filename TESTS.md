# Automated Tests Documentation

## Overview

The backend includes a comprehensive test suite with **50+ test cases** covering all critical functionality:

- ✅ Authentication & Authorization
- ✅ Document CRUD Operations  
- ✅ Permission & Sharing System
- ✅ File Import & Validation
- ✅ Security & Data Sanitization

## Quick Start

### Run All Tests

**Windows:**
```powershell
cd backend
.\run_tests.ps1
```

**Mac/Linux:**
```bash
cd backend
source .venv/bin/activate
pytest
```

### Run Specific Test Suite

```bash
pytest tests/test_auth.py          # Authentication tests
pytest tests/test_documents.py     # Document CRUD tests
pytest tests/test_permissions.py   # Access control tests
pytest tests/test_import.py        # File import tests
```

## Test Coverage

### 🔐 Authentication Tests (`test_auth.py`)

| Test | What It Validates |
|------|------------------|
| `test_login_success` | Valid credentials return token |
| `test_login_invalid_email` | Non-existent email is rejected |
| `test_login_invalid_password` | Wrong password is rejected |
| `test_me_endpoint` | Token returns current user |
| `test_me_endpoint_no_token` | Missing token returns 401 |
| `test_me_endpoint_invalid_token` | Invalid token returns 401 |

### 📄 Document Tests (`test_documents.py`)

| Test | What It Validates |
|------|------------------|
| `test_create_document_default` | Create with default values |
| `test_create_document_with_title` | Create with custom title |
| `test_create_document_with_extension` | Create with file type (.md, .txt, .docx) |
| `test_create_duplicate_documents_auto_rename` | Duplicates renamed (file (2), file (3)) |
| `test_list_documents_empty` | Empty list for new users |
| `test_list_documents_owned` | Owner sees owned documents |
| `test_get_document` | Get specific document by ID |
| `test_get_nonexistent_document` | 404 for missing documents |
| `test_update_document_title` | Title updates work |
| `test_update_document_content` | Content updates work |
| `test_update_document_duplicate_title_fails` | Prevent duplicate titles |
| `test_delete_document` | Delete removes document |
| `test_html_sanitization` | XSS prevention (strips `<script>` tags) |

### 🔒 Permission Tests (`test_permissions.py`)

| Test | What It Validates |
|------|------------------|
| `test_share_document_view_permission` | Share with "view" works |
| `test_share_document_edit_permission` | Share with "edit" works |
| `test_view_only_cannot_edit` | View-only users get 403 on edit |
| `test_non_owner_cannot_delete` | Only owners can delete |
| `test_non_owner_cannot_share` | Only owners can share |
| `test_unshared_document_returns_404` | Unshared docs return 404 (not 403) |
| `test_update_share_permission` | Change view → edit permission |
| `test_revoke_share` | Revoke access removes permission |
| `test_list_shares` | List all people with access |

### 📁 File Import Tests (`test_import.py`)

| Test | What It Validates |
|------|------------------|
| `test_import_txt_file` | Plain text import works |
| `test_import_md_file` | Markdown conversion works |
| `test_import_md_strips_tables` | Tables removed from .md files |
| `test_import_duplicate_filename_auto_rename` | Duplicates renamed on import |
| `test_import_unsupported_extension` | Reject .pdf, .zip, etc. |
| `test_import_file_too_large` | Reject files > 5MB |
| `test_import_empty_file` | Reject empty files |
| `test_import_non_utf8_text` | Reject invalid UTF-8 |
| `test_import_preserves_file_extension` | Extension stored correctly |

## Test Architecture

### Fixtures (Reusable Test Components)

**`test_db`**: Fresh in-memory SQLite database for each test  
**`client`**: TestClient with test database  
**`seed_users`**: Creates Alice, Bob, and Carol test users  
**`alice_token`**: Authentication token for Alice  
**`bob_token`**: Authentication token for Bob  
**`carol_token`**: Authentication token for Carol  

### Test Isolation

Each test runs in complete isolation:
- Fresh database created for each test
- No test affects another test
- Tests can run in any order
- Tests can run in parallel

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Coverage Report

After running tests with coverage:

```bash
pytest --cov=app --cov-report=html
```

Open `backend/htmlcov/index.html` to see:
- Line-by-line coverage
- Which code paths are tested
- Which code paths need tests

## Best Practices

### ✅ DO

- Run tests before committing
- Add tests for new features
- Test both success and failure cases
- Use descriptive test names
- Keep tests independent

### ❌ DON'T

- Skip tests to save time
- Test implementation details
- Make tests depend on each other
- Use production database for tests
- Ignore test failures

## Troubleshooting

### Tests fail with "ModuleNotFoundError"

```bash
cd backend
pip install -r requirements.txt
```

### Tests fail with "database locked"

This shouldn't happen with in-memory databases. If it does, ensure tests aren't sharing database instances.

### Slow tests

Run in parallel:
```bash
pip install pytest-xdist
pytest -n auto
```

## Writing New Tests

Example template:

```python
def test_my_new_feature(client: TestClient, alice_token: str):
    """Test that my feature works correctly."""
    # Arrange - set up test data
    response = client.post(
        "/api/documents",
        json={"title": "Test"},
        headers=auth_headers(alice_token)
    )
    doc_id = response.json()["id"]
    
    # Act - perform the action
    result = client.get(
        f"/api/documents/{doc_id}",
        headers=auth_headers(alice_token)
    )
    
    # Assert - verify the outcome
    assert result.status_code == 200
    assert result.json()["title"] == "Test"
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
