from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class StudioWorkspace(Base):
    __tablename__ = "studio_workspaces"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workspace_name: Mapped[str] = mapped_column(String(255), nullable=False)
    glitch_intensity: Mapped[int] = mapped_column(Integer, nullable=False, default=42)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
