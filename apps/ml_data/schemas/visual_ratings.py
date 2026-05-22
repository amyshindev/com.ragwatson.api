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
    flag: str
    flag_reason: str | None
    rater_type: str
    created_at: datetime
