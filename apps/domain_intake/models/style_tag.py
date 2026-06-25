from datetime import datetime

from database import Base
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class StyleTag(Base):
    """STYLE_TAGS 테이블 ORM — 스타일 태그 마스터 (3NF).

    studio_workspaces.custom_style_tags(varchar_array) 를 분리한 마스터 테이블.
    워크스페이스 ↔ 태그는 WorkspaceStyleTag 조인 테이블로 M:N 연결한다.
    """

    __tablename__ = "style_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # 조인 테이블을 통한 역방향 관계 (lazy=select)
    workspace_links: Mapped[list["WorkspaceStyleTag"]] = relationship(
        "WorkspaceStyleTag", back_populates="style_tag", cascade="all, delete-orphan"
    )


class WorkspaceStyleTag(Base):
    """WORKSPACE_STYLE_TAGS 조인 테이블 ORM (3NF).

    studio_workspaces ↔ style_tags M:N 조인.
    PK: (workspace_id, style_tag_id) 복합 PK.
    CASCADE: workspace 삭제 시 연결 행도 삭제(CASCADE).
             style_tag 삭제 시 연결 행도 삭제(CASCADE).
    """

    __tablename__ = "workspace_style_tags"
    __table_args__ = (
        UniqueConstraint("workspace_id", "style_tag_id", name="uq_workspace_style_tag"),
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("studio_workspaces.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    style_tag_id: Mapped[int] = mapped_column(
        ForeignKey("style_tags.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    style_tag: Mapped["StyleTag"] = relationship("StyleTag", back_populates="workspace_links")
