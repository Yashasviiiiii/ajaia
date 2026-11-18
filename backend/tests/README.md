# Backend Tests

Comprehensive automated tests for the collaborative document API.

## Running Tests

### Install test dependencies:
```bash
cd backend
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Run all tests:
```bash
pytest
```

### Run with coverage report:
```bash
pytest --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in your browser to see detailed coverage.

### Run specific test files:
```bash
pytest tests/test_auth.py
pytest tests/test_permissions.py
pytest tests/test_documents.py
pytest tests/test_import.py
```

### Run specific test:
```bash
pytest tests/test_auth.py::test_login_success
```

### Run tests in parallel (faster):
```bash
pip install pytest-xdist
pytest -n auto
```

## Test Structure

- **`conftest.py`**: Shared fixtures (test database, test client, user tokens)
- **`test_auth.py`**: Authentication endpoints (login, token validation)
- **`test_documents.py`**: Document CRUD operations (create, read, update, delete)
- **`test_permissions.py`**: Access control and sharing (view/edit permissions, owner-only operations)
- **`test_import.py`**: File import functionality (txt, md, docx validation)

## Test Coverage

The tests cover:

✅ **Authentication**
- Successful login
- Invalid credentials
- Token validation
- Unauthorized access

✅ **Document Operations**
- Create with default values
- Create with custom title/content
- Create with file extensions
- Duplicate filename auto-renaming
- List owned and shared documents
- Get, update, delete documents
- HTML sanitization (XSS prevention)

✅ **Access Control**
- Share with view/edit permissions
- Permission enforcement (view-only cannot edit)
- Owner-only operations (delete, share)
- Unshared documents return 404 (not 403)
- Update and revoke shares
- List document shares

✅ **File Import**
- Import .txt, .md files
- Markdown table stripping
- Duplicate filename handling
- File size limits (5MB)
- Unsupported file types
- Invalid UTF-8 rejection
- File extension preservation

## Continuous Integration

To run tests in CI/CD:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    cd backend
    pip install -r requirements.txt
    pytest --cov=app --cov-report=xml
```

## Writing New Tests

1. Add new test files as `tests/test_*.py`
2. Use fixtures from `conftest.py` for common setup
3. Follow naming convention: `test_<what_it_tests>`
4. Use descriptive docstrings
5. Test both success and failure cases

Example:
```python
def test_my_feature(client: TestClient, alice_token: str):
    """Test description of what this validates."""
    response = client.post(
        "/api/endpoint",
        json={"data": "value"},
        headers=auth_headers(alice_token)
    )
    assert response.status_code == 200
    assert response.json()["field"] == "expected"
```
