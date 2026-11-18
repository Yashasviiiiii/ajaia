from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from .content import ImportError_, MAX_UPLOAD_BYTES, import_file, sanitize_html
from .database import get_db
from .models import Document, DocumentShare, User
from .schemas import (
    DocumentCreate,
    DocumentList,
    DocumentOut,
    DocumentSummary,
    DocumentUpdate,
    LoginIn,
    ShareIn,
    ShareOut,
    TokenOut,
    UserOut,
)
from .security import create_token, get_current_user, verify_password

router = APIRouter(prefix="/api")


# ---------- helpers ----------

def _ensure_unique_title(db: Session, title: str, owner_id: int) -> str:
    """Ensure title is unique for this user by appending (2), (3), etc. if needed."""
    base_title = title
    counter = 2
    
    while True:
        # Check if a document with this title exists for this user
        existing = db.scalar(
            select(Document).where(
                Document.owner_id == owner_id,
                Document.title == title
            )
        )
        if existing is None:
            return title
        
        # Title exists, try with counter
        title = f"{base_title} ({counter})"
        counter += 1
        
        # Safety limit to prevent infinite loop
        if counter > 1000:
            # Fallback to timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{base_title}_{timestamp}"


def _summary(doc: Document, role: str) -> DocumentSummary:
    return DocumentSummary(
        id=doc.id,
        title=doc.title,
        file_extension=doc.file_extension,
        updated_at=doc.updated_at,
        owner=UserOut.model_validate(doc.owner),
        role=role,
    )


def _full(doc: Document, role: str) -> DocumentOut:
    return DocumentOut(
        id=doc.id,
        title=doc.title,
        file_extension=doc.file_extension,
        updated_at=doc.updated_at,
        created_at=doc.created_at,
        owner=UserOut.model_validate(doc.owner),
        role=role,
        content=doc.content,
    )


def _get_access(db: Session, doc_id: int, user: User) -> tuple[Document, str]:
    """Return (document, role). Unshared documents look like 404 to avoid leaking existence."""
    doc = db.get(Document, doc_id)
    if doc is None:
        raise HTTPException(404, "Document not found")
    if doc.owner_id == user.id:
        return doc, "owner"
    share = db.scalar(
        select(DocumentShare).where(
            DocumentShare.document_id == doc_id, DocumentShare.user_id == user.id
        )
    )
    if share is None:
        raise HTTPException(404, "Document not found")
    return doc, share.permission


def _require_edit(role: str) -> None:
    if role not in ("owner", "edit"):
        raise HTTPException(403, "You have view-only access to this document")


def _require_owner(role: str) -> None:
    if role != "owner":
        raise HTTPException(403, "Only the owner can do this")


# ---------- auth & users ----------

@router.post("/auth/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email.strip().lower()))
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return TokenOut(access_token=create_token(user.id), user=UserOut.model_validate(user))


@router.get("/auth/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.get("/users", response_model=list[UserOut])
def list_other_users(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(User).where(User.id != user.id).order_by(User.name)).all()


# ---------- documents ----------

@router.get("/documents", response_model=DocumentList)
def list_documents(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    owned = db.scalars(
        select(Document)
        .where(Document.owner_id == user.id)
        .options(selectinload(Document.owner))
        .order_by(Document.updated_at.desc())
    ).all()
    shared_rows = db.execute(
        select(Document, DocumentShare.permission)
        .join(DocumentShare, DocumentShare.document_id == Document.id)
        .where(DocumentShare.user_id == user.id)
        .options(selectinload(Document.owner))
        .order_by(Document.updated_at.desc())
    ).all()
    return DocumentList(
        owned=[_summary(d, "owner") for d in owned],
        shared=[_summary(d, perm) for d, perm in shared_rows],
    )


@router.post("/documents", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def create_document(
    body: DocumentCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    # Set appropriate title based on file type
    if body.file_extension:
        ext = body.file_extension
        if body.title == "Untitled document":
            title = f"Untitled{ext}"
        else:
            title = body.title if body.title.endswith(ext) else f"{body.title}{ext}"
    else:
        title = body.title
    
    unique_title = _ensure_unique_title(db, title, user.id)
    doc = Document(
        title=unique_title,
        content=sanitize_html(body.content),
        file_extension=body.file_extension,
        owner_id=user.id,
        owner=user
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return _full(doc, "owner")


# Declared before /documents/{doc_id} routes for clarity.
@router.post("/documents/import", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def import_document(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = file.file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "File is too large (max 5 MB)")
    if not data:
        raise HTTPException(400, "File is empty")
    try:
        title, content, file_ext = import_file(file.filename or "", data)
    except ImportError_ as exc:
        message = str(exc)
        code = 415 if message.startswith("Unsupported") else 422
        raise HTTPException(code, message)

    unique_title = _ensure_unique_title(db, title, user.id)
    doc = Document(
        title=unique_title,
        content=content,
        file_extension=file_ext,
        owner_id=user.id,
        owner=user
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return _full(doc, "owner")


@router.get("/documents/{doc_id}", response_model=DocumentOut)
def get_document(
    doc_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    doc, role = _get_access(db, doc_id, user)
    return _full(doc, role)


@router.patch("/documents/{doc_id}", response_model=DocumentOut)
def update_document(
    doc_id: int,
    body: DocumentUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc, role = _get_access(db, doc_id, user)
    _require_edit(role)
    if body.title is not None:
        # Check if the new title would create a duplicate (excluding current doc)
        existing = db.scalar(
            select(Document).where(
                Document.owner_id == doc.owner_id,
                Document.title == body.title,
                Document.id != doc.id
            )
        )
        if existing:
            raise HTTPException(400, f"You already have a document named '{body.title}'")
        doc.title = body.title
    if body.content is not None:
        doc.content = sanitize_html(body.content)
    db.commit()
    db.refresh(doc)
    return _full(doc, role)


@router.delete("/documents/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    doc_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    doc, role = _get_access(db, doc_id, user)
    _require_owner(role)
    db.delete(doc)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------- sharing ----------

@router.get("/documents/{doc_id}/shares", response_model=list[ShareOut])
def list_shares(
    doc_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    doc, role = _get_access(db, doc_id, user)
    _require_owner(role)
    return [
        ShareOut(user=UserOut.model_validate(s.user), permission=s.permission)
        for s in doc.shares
    ]


@router.post("/documents/{doc_id}/shares", response_model=ShareOut)
def share_document(
    doc_id: int,
    body: ShareIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc, role = _get_access(db, doc_id, user)
    _require_owner(role)
    target = db.scalar(select(User).where(User.email == body.email.strip().lower()))
    if target is None:
        raise HTTPException(404, "No user with that email")
    if target.id == doc.owner_id:
        raise HTTPException(400, "The owner already has full access")

    share = db.scalar(
        select(DocumentShare).where(
            DocumentShare.document_id == doc.id, DocumentShare.user_id == target.id
        )
    )
    if share:
        share.permission = body.permission
    else:
        db.add(DocumentShare(document_id=doc.id, user_id=target.id, permission=body.permission))
    db.commit()
    return ShareOut(user=UserOut.model_validate(target), permission=body.permission)


@router.delete("/documents/{doc_id}/shares/{target_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_share(
    doc_id: int,
    target_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc, role = _get_access(db, doc_id, user)
    _require_owner(role)
    share = db.scalar(
        select(DocumentShare).where(
            DocumentShare.document_id == doc.id, DocumentShare.user_id == target_id
        )
    )
    if share is None:
        raise HTTPException(404, "Share not found")
    db.delete(share)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)