from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AudioUploadCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    source_type: str = Field(..., min_length=1)
    original_filename: str | None = None
    source_url: str | None = None
    storage_path: str | None = None
    file_size_bytes: int | None = Field(None, ge=0)
    duration_sec: float | None = Field(None, ge=0.0)
    mime_type: str | None = None
    processing_status: str = "pending"
    error_message: str | None = None
    audio_feature_id: UUID | None = None


class AudioUploadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: int
    source_type: str
    original_filename: str | None
    source_url: str | None
    storage_path: str | None
    file_size_bytes: int | None
    duration_sec: float | None
    mime_type: str | None
    processing_status: str
    error_message: str | None
    audio_feature_id: UUID | None
    created_at: datetime


class AudioUploadStatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    processing_status: str
    error_message: str | None
    audio_feature_id: UUID | None
    created_at: datetime
