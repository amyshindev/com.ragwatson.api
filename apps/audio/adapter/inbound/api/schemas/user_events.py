from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserEventCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    session_id: str | None = None
    event_type: str = Field(..., min_length=1, max_length=50)
    target_id: UUID | None = None
    target_type: str | None = None
    dwell_ms: int | None = Field(None, ge=0)
    payload: dict[str, Any] | None = None


class UserEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: int
    session_id: str | None
    event_type: str
    target_id: UUID | None
    target_type: str | None
    dwell_ms: int | None
    payload: dict[str, Any] | None
    created_at: datetime
