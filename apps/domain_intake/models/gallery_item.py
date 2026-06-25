from datetime import datetime

from database import Base
from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column


class GalleryItem(Base):
    __tablename__ = "gallery_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    work_title: Mapped[str] = mapped_column(String(255), nullable=False)
    artist: Mapped[str] = mapped_column(String(255), nullable=False)
    # genre_tags 제거 — v4: GENRES + GALLERY_ITEM_GENRES 조인 테이블로 3NF 분리
    media_url: Mapped[str | None] = mapped_column(Text, nullable=True)
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
