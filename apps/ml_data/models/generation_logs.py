import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class GenerationLog(Base):
    __tablename__ = "generation_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("studio_workspaces.id"), nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False, index=True
    )
    audio_feature_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("audio_features.id"), nullable=True
    )

    prompt_params: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pipeline_version: Mapped[str | None] = mapped_column(String(50), nullable=True)

    output_asset_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    render_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    style_vector: Mapped[list[float] | None] = mapped_column(ARRAY(Float), nullable=True)

    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    audio_feature: Mapped["AudioFeature | None"] = relationship(
        "AudioFeature", back_populates="generation_logs"
    )
    visual_ratings: Mapped[list["VisualRating"]] = relationship(
        "VisualRating", back_populates="generation_log"
    )
