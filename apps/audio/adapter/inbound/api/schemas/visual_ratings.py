from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class VisualRatingCreate(BaseModel):
    rater_id: int = Field(..., ge=1)
    generation_id: UUID
    aesthetic_score: int | None = Field(None, ge=1, le=5)
    genre_match_score: int | None = Field(None, ge=1, le=5)
    mood_match_score: int | None = Field(None, ge=1, le=5)
    ab_test_id: str | None = None
    ab_winner: bool | None = None
    platform: str | None = None
    loop_smoothness_score: int | None = Field(None, ge=1, le=5)
    beat_sync_score: int | None = Field(None, ge=1, le=5)
    flag: str = "ok"
    flag_reason: str | None = None
    rater_type: str = "user"


class VisualRatingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    generation_id: UUID
    rater_id: int
    aesthetic_score: int | None
    genre_match_score: int | None
    mood_match_score: int | None
    ab_test_id: str | None
    ab_winner: bool | None
    platform: str | None
    loop_smoothness_score: int | None
    beat_sync_score: int | None
    flag: str
    flag_reason: str | None
    rater_type: str
    created_at: datetime


class VisualRatingAvgRead(BaseModel):
    generation_id: UUID
    avg_aesthetic: float | None
    avg_genre_match: float | None
    avg_mood_match: float | None
    total_count: int


class AbTestResultRead(BaseModel):
    ab_test_id: str
    winner_generation_id: UUID | None
    win_count: int
    lose_count: int


class VisualRatingPlatformAvgRead(BaseModel):
    generation_id: UUID
    platform: str | None
    avg_loop_smoothness: float | None
    avg_beat_sync: float | None
    total_count: int
