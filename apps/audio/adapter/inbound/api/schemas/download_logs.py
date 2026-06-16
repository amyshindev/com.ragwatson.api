from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DownloadLogCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    asset_id: UUID
    ip_address: str | None = None


class DownloadLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: int
    asset_id: UUID
    ip_address: str | None
    downloaded_at: datetime
