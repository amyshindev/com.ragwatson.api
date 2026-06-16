from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class TrainingRecord(BaseModel):
    audio_feature_id: UUID
    bpm: float | None = None
    energy: float | None = None
    valence: float | None = None
    danceability: float | None = None
    spectral_centroid: float | None = None
    loudness: float | None = None
    genre_primary: str | None = None
    mood_tags: list[str] | None = None
    beat_timestamps: list[float] | None = None
    highlight_start_sec: float | None = None
    highlight_end_sec: float | None = None
    onset_strength: float | None = None
    visual_motion_intensity: float | None = None
    visual_texture_type: str | None = None
    visual_color_temperature: str | None = None
    visual_rhythm_sync: float | None = None
    genre_to_visual_mapping: dict[str, Any] | None = None
    mood_to_color_mapping: dict[str, Any] | None = None
    predicted_visual_style: str | None = None
    predicted_color_palette: list[str] | None = None
    visual_embedding: list[float] | None = None
    prompt_params: dict[str, Any] | None = None
    model_version: str | None = None
    platform_id: int | None = None
    loop_duration_sec: float | None = None
    loop_beat_aligned: bool | None = None
    frame_rate: int | None = None
    aesthetic_score: int | None = None
    genre_match_score: int | None = None
    mood_match_score: int | None = None
    loop_smoothness_score: int | None = None
    beat_sync_score: int | None = None
    rating_platform_id: int | None = None
    ab_winner: bool | None = None


class DatasetStatsRead(BaseModel):
    total_audio_features: int
    total_generation_logs: int
    total_ratings: int
    avg_aesthetic_score: float | None
    avg_loop_smoothness: float | None
    avg_beat_sync: float | None
    labeled_count: int
    platform_breakdown: dict[str, int] = Field(default_factory=dict)
