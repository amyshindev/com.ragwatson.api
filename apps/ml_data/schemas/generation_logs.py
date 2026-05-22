from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GenerationLogCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    workspace_id: int | None = None
    audio_feature_id: UUID | None = None
    prompt_params: dict[str, Any] | None = None
    model_version: str | None = None
    pipeline_version: str | None = None
    output_asset_url: str | None = None
    render_ms: int | None = Field(None, ge=0)
    quality_score: float | None = None
    style_vector: list[float] | None = None
    status: str = "pending"
    error_message: str | None = None


class GenerationLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: int
    workspace_id: int | None
    audio_feature_id: UUID | None
    prompt_params: dict[str, Any] | None
    model_version: str | None
    pipeline_version: str | None
    output_asset_url: str | None
    render_ms: int | None
    quality_score: float | None
    style_vector: list[float] | None
    status: str
    error_message: str | None
    created_at: datetime
    completed_at: datetime | None
