from datetime import datetime

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class PlatformSpec(Base):
    """PLATFORM_SPECS 테이블 ORM — 플랫폼 마스터 (3NF).

    generation_logs.target_platform, generation_assets.platform 의
    이행 종속(platform → aspect_ratio, resolution)을 해소하기 위해
    분리한 마스터 테이블.

    시드 데이터 (Alembic 마이그레이션에서 INSERT):
        spotify_canvas | 9:16 | 1080x1920 | 8.0
        tiktok         | 9:16 | 1080x1920 | 15.0
        shorts         | 9:16 | 1080x1920 | 60.0
        universal      | 1:1  | 1080x1080 | 30.0
    """

    __tablename__ = "platform_specs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    platform_name: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    default_aspect_ratio: Mapped[str | None] = mapped_column(String(10), nullable=True)
    default_resolution: Mapped[str | None] = mapped_column(String(30), nullable=True)
    default_duration_sec: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
