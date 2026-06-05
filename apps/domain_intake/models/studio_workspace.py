from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class StudioWorkspace(Base):
    __tablename__ = "studio_workspaces"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )  # v4 신규 — 워크스페이스 소유자 FK
    workspace_name: Mapped[str] = mapped_column(String(255), nullable=False)
    glitch_intensity: Mapped[int] = mapped_column(Integer, nullable=False, default=42)
    neon_palette: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fragmentation_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    aspect_ratio: Mapped[str | None] = mapped_column(String(10), nullable=True)
    # custom_style_tags 제거 — v4: STYLE_TAGS + WORKSPACE_STYLE_TAGS 조인 테이블로 3NF 분리
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
