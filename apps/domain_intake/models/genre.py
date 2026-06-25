from datetime import datetime

from database import Base
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Genre(Base):
    """GENRES 테이블 ORM — 장르 마스터 (3NF).

    gallery_items.genre_tags(varchar) 를 분리한 마스터 테이블.
    갤러리 아이템 ↔ 장르는 GalleryItemGenre 조인 테이블로 M:N 연결한다.
    """

    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    genre_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # 조인 테이블을 통한 역방향 관계
    gallery_links: Mapped[list["GalleryItemGenre"]] = relationship(
        "GalleryItemGenre", back_populates="genre"
    )


class GalleryItemGenre(Base):
    """GALLERY_ITEM_GENRES 조인 테이블 ORM (3NF).

    gallery_items ↔ genres M:N 조인.
    PK: (gallery_item_id, genre_id) 복합 PK.
    CASCADE: gallery_item 삭제 시 연결 행도 삭제(CASCADE).
             genre 삭제는 RESTRICT (참조 중이면 불가).
    """

    __tablename__ = "gallery_item_genres"
    __table_args__ = (
        UniqueConstraint("gallery_item_id", "genre_id", name="uq_gallery_item_genre"),
    )

    gallery_item_id: Mapped[int] = mapped_column(
        ForeignKey("gallery_items.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.id", ondelete="RESTRICT"),
        primary_key=True,
        nullable=False,
    )

    genre: Mapped["Genre"] = relationship("Genre", back_populates="gallery_links")
