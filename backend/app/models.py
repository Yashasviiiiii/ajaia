from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def _now() -> datetime:
    # Stored as naive UTC; schemas re-attach the UTC timezone on output.
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(255))


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), default="Untitled document")
    content: Mapped[str] = mapped_column(Text, default="")
    file_extension: Mapped[str | None] = mapped_column(String(10), default=None)  # .txt, .md, .docx, or None for native docs
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now, onupdate=_now)

    owner: Mapped[User] = relationship()
    shares: Mapped[list["DocumentShare"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )


class DocumentShare(Base):
    __tablename__ = "document_shares"
    __table_args__ = (UniqueConstraint("document_id", "user_id", name="uq_share_doc_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    permission: Mapped[str] = mapped_column(String(10))  # "view" | "edit"

    document: Mapped[Document] = relationship(back_populates="shares")
    user: Mapped[User] = relationship()