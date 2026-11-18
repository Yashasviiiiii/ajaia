# Docs: Collaborative Document Editor

A lightweight Google Docs-style application for creating, editing, and sharing documents. Choose your document type (Word, Markdown, or Plain Text), edit with real-time formatting, and collaborate with team members through a robust permission system.

Built with **FastAPI + SQLite** backend and **React + Tiptap** frontend.

**Key Features:**
- 📄 Multiple document types (.docx, .md, .txt) with type-aware features
- 🔒 Granular permission control (view/edit/owner)
- 📤 File import with auto-conversion
- ✨ Rich text editing with autosave
- 🔐 Multi-tab login with independent sessions
- 🛡️ Comprehensive security (XSS prevention, duplicate prevention)
- ✅ 50+ automated tests with full coverage

---

## Quick Start

**Requirements:** Python 3.10+, Node 18+

### Windows
```powershell
.\run.ps1
```

### Mac/Linux
```bash
chmod +x run.sh
./run.sh
 or
bash run.sh
```

Then open **http://localhost:5173**

The script sets up virtualenv, installs dependencies, and starts both servers. First run takes ~1 minute.

### Manual Setup

**Terminal 1: Backend**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Terminal 2: Frontend**
```bash
cd frontend
npm install
npm run dev
```

API docs: http://localhost:8000/docs  
App: http://localhost:5173

---

## Testing

Run the comprehensive test suite covering authentication, permissions, documents, and imports:

```bash
cd backend
pip install -r requirements.txt
pytest
```

Generate coverage report:
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

**Windows:** Run `backend\run_tests.ps1`

See `TESTS.md` and `backend/tests/README.md` for details.

---

## Demo Accounts

Three users pre-seeded with password `password123`:

| User  | Email             |
|-------|-------------------|
| Alice | alice@example.com |
| Bob   | bob@example.com   |
| Carol | carol@example.com |

Login buttons on the page auto-fill these credentials. **Multi-tab support:** Open multiple tabs to login as different users simultaneously.

---

## Feature Walkthrough

### Document Types

When creating a document, choose one:

1. **Word Document (.docx)** - Full features with tables, all formatting
2. **Markdown Document (.md)** - Simple formatting, no tables
3. **Plain Text Document (.txt)** - Basic text only, no tables

Document type determines which editor features are available and is shown as a badge in the dashboard.

### Creating & Editing Documents

- Click **"+ New document"** → select document type
- Edit title inline or via double-click
- Autosave triggers ~0.8s after typing stops
- Status indicator shows: "Saving…", "All changes saved", "Save failed"
- Unsaved changes trigger browser warning on tab close

**Available formatting:**
- Bold, Italic, Underline
- Heading 1, 2, 3
- Bulleted and numbered lists
- Tables (Word documents only)
- Undo/Redo

### File Upload

Upload .txt, .md, or .docx files (max 5 MB):

- **Plain text:** Preserves paragraphs and line breaks
- **Markdown:** Converts to HTML; tables are stripped
- **Word:** Preserves headings, formatting, lists, and tables; images skipped

Duplicate filenames auto-rename: `notes.md` → `notes.md (2)` → `notes.md (3)`

### Sharing & Permissions

**Owner controls:**
- Share with other users (view-only or editable)
- Change permissions anytime
- Revoke access
- Delete documents

**Permission levels:**
- **Owner:** Full control (share, delete, edit)
- **Can edit:** Edit document content, but not share
- **View only:** Read-only, cannot edit

**Security features:**
- Unshared documents return 404 (not 403) to prevent existence leaking
- Permissions enforced server-side (UI only a convenience)
- All HTML sanitized to prevent XSS attacks

---

## What It Does

### Documents
- Create via type selector dialog or upload files
- Edit with real-time formatting feedback
- Autosave with visible status
- Rename and delete (owner only)
- Prevent duplicate filenames automatically
- Display file type badges (.docx, .md, .txt)

### Sharing & Access
- Share with view or edit permissions
- Update permissions after sharing
- Revoke access instantly
- Dashboard separates owned vs. shared documents
- Role badges on every document

### Sessions
- Multi-tab support: login as different users per tab
- Session cleared on tab close
- No data shared between tabs

### File Import
- Convert uploaded files to editable documents
- Auto-title from filename + extension
- Strip unsupported elements (tables from .md, images from .docx)
- Validate file size and encoding
- Auto-rename duplicates

---

## Architecture

### Directory Structure
```
ajaia-docs/
├── run.ps1                      # Windows startup script
├── run.sh                       # Mac/Linux startup script
├── README.md                    # This file
├── TESTS.md                     # Testing guide
├── backend/
│   ├── requirements.txt         # Python dependencies
│   ├── pytest.ini              # Test configuration
│   ├── run_tests.ps1           # Windows test runner
│   ├── app/
│   │   ├── main.py             # FastAPI app + startup hooks
│   │   ├── database.py         # SQLAlchemy setup
│   │   ├── models.py           # Database models
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── security.py         # Auth & password hashing
│   │   ├── content.py          # File import & HTML sanitization
│   │   └── routes.py           # All API endpoints
│   └── tests/
│       ├── conftest.py         # Pytest fixtures
│       ├── test_auth.py        # Authentication (6 tests)
│       ├── test_documents.py   # CRUD operations (14 tests)
│       ├── test_permissions.py # Access control (11 tests)
│       ├── test_import.py      # File import (10 tests)
│       └── README.md           # Test documentation
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── constants.js        # Shared constants
        ├── main.jsx
        ├── App.jsx             # Routing
        ├── auth.jsx            # Auth context
        ├── api.js              # API client
        ├── Login.jsx
        ├── Dashboard.jsx       # Document list & create
        ├── EditorPage.jsx      # Editor with autosave
        ├── Toolbar.jsx         # Formatting controls
        ├── ShareDialog.jsx     # Sharing UI
        └── styles.css
```

### Data Model

**users**
- id (primary key)
- email (unique)
- name
- password_hash

**documents**
- id (primary key)
- title
- content (sanitized HTML)
- file_extension (.txt/.md/.docx or null)
- owner_id (foreign key)
- created_at, updated_at

**document_shares**
- id (primary key)
- document_id, user_id (foreign keys, unique pair)
- permission (view or edit)

### API Routes

All routes under `/api`. Except login, all require Bearer token.

**Authentication**
```
POST   /auth/login          # { email, password } → { access_token, user }
GET    /auth/me             # Current user info
GET    /users               # List all users
```

**Documents**
```
GET    /documents           # { owned, shared }
POST   /documents           # Create { title, content?, file_extension? }
POST   /documents/import    # Upload file → new document
GET    /documents/{id}      # Get document
PATCH  /documents/{id}      # Update { title?, content? }
DELETE /documents/{id}      # Delete (owner only)
```

**Sharing**
```
GET    /documents/{id}/shares              # List shares
POST   /documents/{id}/shares              # Add/update { email, permission }
DELETE /documents/{id}/shares/{userId}     # Revoke (owner only)
```

---

## Design Decisions

### Storage & Sanitization
HTML is stored directly (Tiptap → HTML → DB → HTML → Tiptap). Content sanitized server-side on all writes to prevent XSS via `bleach` allow-list.

### Permissions
Enforced server-side as the real gatekeeper:
- 404 for unshared documents (not 403) to prevent existence leaking
- 403 for access denied on shared documents
- Buttons hidden on UI but API validates all requests

### Multi-Tab Sessions
Uses `sessionStorage` instead of `localStorage`:
- Each tab gets independent session
- Tab-specific login/logout
- No data shared across tabs
- Cleared on tab close

### Document Types
File extensions stored to determine features:
- .docx = tables + rich formatting
- .md/.txt = no tables, simpler toolbar

### Autosave
Debounced 0.8s after typing with status feedback. Failures visible and retried instead of silent.

### Duplicate Prevention
Automatic renaming: `file.md`, `file.md (2)`, `file.md (3)`. Manual rename rejects duplicates with clear error message.

---

## Configuration

| Variable | Default | Notes |
|----------|---------|-------|
| `SECRET_KEY` | dev-secret | JWT signing key. **Change for production.** |
| `DATABASE_URL` | sqlite:///./app.db | Database location. |

Reset all data:
```bash
rm backend/app.db
# Restart app - recreates and re-seeds
```

---

## Testing

### What's Tested (50+ cases)

✅ **Authentication** - Login, tokens, access control (6 tests)  
✅ **Documents** - CRUD, autosave, duplicate prevention (14 tests)  
✅ **Permissions** - Share, view/edit/owner roles, security (11 tests)  
✅ **File Import** - .txt/.md/.docx, validation, tables (10 tests)

### Run Tests

```bash
cd backend
pytest                                    # All tests
pytest tests/test_auth.py                # Specific file
pytest tests/test_auth.py::test_login_success  # Specific test
pytest --cov=app --cov-report=html       # With coverage
```

---

## Known Limitations

- **No real-time collaboration.** Last-write-wins on concurrent edits. Would need CRDT/OT (e.g., Yjs) + WebSockets.
- **No email-based sharing.** Share from pre-populated user list. Production would need email lookup or directory.
- **Sessions cleared per tab.** No persistent sessions across tabs (by design for multi-user support).
- **No password reset or sign-up.** Fixed demo accounts only.
- **Limited import scope.** No .docx nested lists, no export to PDF/.docx.
- **SQLite only.** Suitable for single-node demo. Postgres + migrations (Alembic) for production.
- **No version history or comments.**
- **No links, images, colors, or fonts in editor.**

---

## Enhancements that can be done

1. Real-time collaboration with Yjs + WebSockets
2. Email-based user discovery for sharing
3. Version history and restore
4. Export to PDF, .docx
5. Comments and mentions
6. Rich formatting (links, images, colors, fonts)
7. Search across documents
8. User activity log