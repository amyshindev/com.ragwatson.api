from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AudioFeatureCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    workspace_id: int | None = None
    bpm: float | None = Field(None, ge=20, le=300)
    energy: float | None = Field(None, ge=0.0, le=1.0)
    valence: float | None = Field(None, ge=0.0, le=1.0)
    danceability: float | None = Field(None, ge=0.0, le=1.0)
    spectral_centroid: float | None = None
    loudness: float | None = None
    key: int | None = Field(None, ge=0, le=11)
    mode: int | None = Field(None, ge=0, le=1)
    genre_primary: str | None = None
    genre_secondary: str | None = None
    mood_tags: list[str] | None = None
    source: str = "upload"
    source_url: str | None = None
    duration_sec: float | None = None


class AudioFeatureRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: int
    workspace_id: int | None
    bpm: float | None
    energy: float | None
    valence: float | None
    danceability: float | None
    spectral_centroid: float | None
    loudness: float | None
    key: int | None
    mode: int | None
    genre_primary: str | None
    genre_secondary: str | None
    mood_tags: list[str] | None
    source: str
    source_url: str | None
    duration_sec: float | None
    created_at: datetime
