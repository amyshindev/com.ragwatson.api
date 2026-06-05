from datetime import datetime
from typing import Any
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
    processing_status: str
    error_message: str | None
    predicted_visual_style: str | None
    predicted_color_palette: list[str] | None
    visual_embedding: list[float] | None
    model_version: str | None
    inferred_at: datetime | None
    visual_motion_intensity: float | None
    visual_texture_type: str | None
    visual_color_temperature: str | None
    visual_rhythm_sync: float | None
    genre_to_visual_mapping: dict[str, Any] | None
    mood_to_color_mapping: dict[str, Any] | None
    beat_timestamps: list[float] | None
    highlight_start_sec: float | None
    highlight_end_sec: float | None
    onset_strength: float | None
    created_at: datetime


class AudioFeatureStatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    processing_status: str
    error_message: str | None
    created_at: datetime
    inferred_at: datetime | None


class AudioFeatureVisualRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    visual_motion_intensity: float | None
    visual_texture_type: str | None
    visual_color_temperature: str | None
    visual_rhythm_sync: float | None
    genre_to_visual_mapping: dict[str, Any] | None
    mood_to_color_mapping: dict[str, Any] | None
    beat_timestamps: list[float] | None
    highlight_start_sec: float | None
    highlight_end_sec: float | None
    onset_strength: float | None
