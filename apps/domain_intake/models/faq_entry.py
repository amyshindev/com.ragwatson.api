from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class FaqEntry(Base):
    __tablename__ = "faq_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str | None] = mapped_column(String(128), nullable=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
