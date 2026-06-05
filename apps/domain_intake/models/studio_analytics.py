from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class StudioAnalytics(Base):
    __tablename__ = "studio_analytics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    track_title: Mapped[str] = mapped_column(String(255), nullable=False)
    bpm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mood: Mapped[str | None] = mapped_column(String(64), nullable=True)
    genre: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("admins.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )  # v4: users(id) → admins(id)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
