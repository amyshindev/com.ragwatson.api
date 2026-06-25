from __future__ import annotations

from datetime import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.oracle_database import Base


class UserEvent(Base):
    __tablename__ = "user_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False, index=True
    )
    session_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    target_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    dwell_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
