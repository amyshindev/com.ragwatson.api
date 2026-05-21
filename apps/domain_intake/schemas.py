"""마케팅·도메인 폼 제출용 요청·응답 DTO."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, BeforeValidator, EmailStr, Field, field_validator


def _blank_to_none(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, str) and v.strip() == "":
        return None
    return v


OptionalStr = Annotated[str | None, BeforeValidator(_blank_to_none)]


class DomainAcceptedResponse(BaseModel):
    ok: Literal[True] = True
    id: int
    kind: str


class LibraryCreate(BaseModel):
    projectTitle: str = Field(..., min_length=1, description="프로젝트 이름")
    memo: OptionalStr = None
    tags: OptionalStr = None


class StudioWorkspaceCreate(BaseModel):
    workspaceName: str = Field(..., min_length=1)
    glitchIntensity: int = Field(default=42, ge=0, le=100)
    notes: OptionalStr = None


class StudioAnalyticsCreate(BaseModel):
    trackTitle: str = Field(..., min_length=1)
    bpm: int | None = Field(default=None, ge=1)
    mood: OptionalStr = None
    genre: OptionalStr = None

    @field_validator("bpm", mode="before")
    @classmethod
    def coerce_empty_bpm(cls, v: object) -> object:
        if v is None or v == "":
            return None
        return v


class MembershipInquiryCreate(BaseModel):
    email: EmailStr
    plan: Literal["free", "pro", "team"]
    message: OptionalStr = None


class GalleryCreate(BaseModel):
    workTitle: str = Field(..., min_length=1)
    artist: str = Field(..., min_length=1)
    genreTags: OptionalStr = None
    mediaUrl: OptionalStr = None


class MagazineCreate(BaseModel):
    articleTitle: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    excerpt: OptionalStr = None
    body: OptionalStr = None


class FaqCreate(BaseModel):
    category: OptionalStr = None
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)
