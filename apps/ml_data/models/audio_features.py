import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


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

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    generation_logs: Mapped[list["GenerationLog"]] = relationship(
        "GenerationLog", back_populates="audio_feature"
    )
