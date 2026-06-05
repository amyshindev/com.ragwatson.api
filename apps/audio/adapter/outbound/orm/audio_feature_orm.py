from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.matrix.oracle_database import Base

if TYPE_CHECKING:
    from audio.adapter.outbound.orm.generation_log_orm import GenerationLog


class AudioFeature(Base):
    __tablename__ = "audio_features"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("studio_workspaces.id"), nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False, index=True
    )

    bpm: Mapped[float | None] = mapped_column(Float, nullable=True)
    energy: Mapped[float | None] = mapped_column(Float, nullable=True)
    valence: Mapped[float | None] = mapped_column(Float, nullable=True)
    danceability: Mapped[float | None] = mapped_column(Float, nullable=True)
    spectral_centroid: Mapped[float | None] = mapped_column(Float, nullable=True)
    loudness: Mapped[float | None] = mapped_column(Float, nullable=True)
    key: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mode: Mapped[int | None] = mapped_column(Integer, nullable=True)

    genre_primary: Mapped[str | None] = mapped_column(String(100), nullable=True)
    genre_secondary: Mapped[str | None] = mapped_column(String(100), nullable=True)
    mood_tags: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    source: Mapped[str] = mapped_column(String(50), nullable=False, default="upload")
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    duration_sec: Mapped[float | None] = mapped_column(Float, nullable=True)

    processing_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="pending"
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    predicted_visual_style: Mapped[str | None] = mapped_column(String(100), nullable=True)
    predicted_color_palette: Mapped[list[str] | None] = mapped_column(
        ARRAY(String), nullable=True
    )
    visual_embedding: Mapped[list[float] | None] = mapped_column(ARRAY(Float), nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    inferred_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    visual_motion_intensity: Mapped[float | None] = mapped_column(Float, nullable=True)
    visual_texture_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    visual_color_temperature: Mapped[str | None] = mapped_column(String(50), nullable=True)
    visual_rhythm_sync: Mapped[float | None] = mapped_column(Float, nullable=True)
    genre_to_visual_mapping: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    mood_to_color_mapping: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    beat_timestamps: Mapped[list[float] | None] = mapped_column(ARRAY(Float), nullable=True)
    highlight_start_sec: Mapped[float | None] = mapped_column(Float, nullable=True)
    highlight_end_sec: Mapped[float | None] = mapped_column(Float, nullable=True)
    onset_strength: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    generation_logs: Mapped[list[GenerationLog]] = relationship(
        back_populates="audio_feature",
    )
