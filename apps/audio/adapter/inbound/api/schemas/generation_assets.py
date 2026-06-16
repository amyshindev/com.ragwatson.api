from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GenerationAssetCreate(BaseModel):
    generation_id: UUID
    platform_id: int = Field(..., ge=1)
    resolution: str | None = None
    asset_type: str = Field(..., min_length=1)
    file_size_bytes: int | None = Field(None, ge=0)
    storage_url: str | None = None
    expires_at: datetime | None = None
    download_count: int = Field(0, ge=0)


class GenerationAssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    generation_id: UUID
    platform_id: int
    resolution: str | None
    asset_type: str
    file_size_bytes: int | None
    storage_url: str | None
    expires_at: datetime | None
    download_count: int
    created_at: datetime
