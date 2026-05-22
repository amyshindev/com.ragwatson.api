import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class VisualRating(Base):
    __tablename__ = "visual_ratings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    generation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("generation_logs.id"), nullable=False
    )
    rater_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False, index=True
    )

    aesthetic_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    genre_match_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mood_match_score: Mapped[int | None] = mapped_column(Integer, nullable=True)

    ab_test_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ab_winner: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    flag: Mapped[str] = mapped_column(String(30), nullable=False, default="ok")
    flag_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    rater_type: Mapped[str] = mapped_column(String(20), nullable=False, default="user")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    generation_log: Mapped["GenerationLog"] = relationship(
        "GenerationLog", back_populates="visual_ratings"
    )
