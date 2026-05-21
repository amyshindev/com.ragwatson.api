from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class LibraryItem(Base):
    __tablename__ = "library_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_title: Mapped[str] = mapped_column(String(255), nullable=False)
    memo: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
