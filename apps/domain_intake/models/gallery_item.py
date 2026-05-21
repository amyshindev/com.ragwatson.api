from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class GalleryItem(Base):
    __tablename__ = "gallery_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    work_title: Mapped[str] = mapped_column(String(255), nullable=False)
    artist: Mapped[str] = mapped_column(String(255), nullable=False)
    genre_tags: Mapped[str | None] = mapped_column(String(512), nullable=True)
    media_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
