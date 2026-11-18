from datetime import datetime, timezone
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, PlainSerializer, StringConstraints


def _as_utc_iso(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


UTCDateTime = Annotated[datetime, PlainSerializer(_as_utc_iso, return_type=str)]
Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
Permission = Literal["view", "edit"]
Role = Literal["owner", "edit", "view"]

MAX_CONTENT_CHARS = 2_000_000


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str


class LoginIn(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    user: UserOut


class DocumentCreate(BaseModel):
    title: Title = "Untitled document"
    content: Annotated[str, StringConstraints(max_length=MAX_CONTENT_CHARS)] = ""
    file_extension: Optional[Literal[".txt", ".md", ".docx"]] = None


class DocumentUpdate(BaseModel):
    title: Optional[Title] = None
    content: Optional[Annotated[str, StringConstraints(max_length=MAX_CONTENT_CHARS)]] = None


class DocumentSummary(BaseModel):
    id: int
    title: str
    file_extension: Optional[str] = None
    updated_at: UTCDateTime
    owner: UserOut
    role: Role


class DocumentOut(DocumentSummary):
    content: str
    created_at: UTCDateTime


class DocumentList(BaseModel):
    owned: list[DocumentSummary]
    shared: list[DocumentSummary]


class ShareIn(BaseModel):
    email: str
    permission: Permission


class ShareOut(BaseModel):
    user: UserOut
    permission: Permission