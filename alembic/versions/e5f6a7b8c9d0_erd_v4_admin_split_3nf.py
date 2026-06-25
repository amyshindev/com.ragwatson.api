"""erd_v4_admin_split_3nf

Admin/User 완전 분리 + 3NF 적용 마이그레이션.

변경 내용:
  1.  CREATE TABLE admins
  2.  CREATE TABLE platform_specs + 시드 INSERT
  3.  CREATE TABLE style_tags
  4.  CREATE TABLE workspace_style_tags
  5.  CREATE TABLE genres
  6.  CREATE TABLE gallery_item_genres
  7.  ALTER TABLE users  — role 컬럼 DROP, deleted_at ADD
  8.  ALTER TABLE studio_workspaces — user_id FK ADD, neon_palette/fragmentation_level/aspect_ratio ADD, custom_style_tags DROP (컬럼 없으면 skip)
  9.  ALTER TABLE gallery_items — genre_tags DROP, created_by FK → admins 변경
  10. ALTER TABLE faq_entries    — created_by FK → admins 추가
  11. ALTER TABLE magazine_articles — created_by FK → admins 추가
  12. ALTER TABLE studio_analytics  — created_by FK → admins 추가

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-06-05
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "e5f6a7b8c9d0"
down_revision: str | Sequence[str] | None = "d4e5f6a7b8c9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# ──────────────────────────────────────────────────────────────────────────────
# 시드 데이터
# ──────────────────────────────────────────────────────────────────────────────
_PLATFORM_SEED = [
    {
        "platform_name": "spotify_canvas",
        "default_aspect_ratio": "9:16",
        "default_resolution": "1080x1920",
        "default_duration_sec": 8.0,
    },
    {
        "platform_name": "tiktok",
        "default_aspect_ratio": "9:16",
        "default_resolution": "1080x1920",
        "default_duration_sec": 15.0,
    },
    {
        "platform_name": "shorts",
        "default_aspect_ratio": "9:16",
        "default_resolution": "1080x1920",
        "default_duration_sec": 60.0,
    },
    {
        "platform_name": "universal",
        "default_aspect_ratio": "1:1",
        "default_resolution": "1080x1080",
        "default_duration_sec": 30.0,
    },
]


def upgrade() -> None:
    # ── 1. admins 테이블 생성 ─────────────────────────────────────────────────
    op.create_table(
        "admins",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("username", sa.String(64), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_admins_email", "admins", ["email"], unique=True)

    # ── 2. platform_specs 테이블 생성 + 시드 ──────────────────────────────────
    op.create_table(
        "platform_specs",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("platform_name", sa.String(50), unique=True, nullable=False),
        sa.Column("default_aspect_ratio", sa.String(10), nullable=True),
        sa.Column("default_resolution", sa.String(30), nullable=True),
        sa.Column("default_duration_sec", sa.Float(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_platform_specs_name", "platform_specs", ["platform_name"], unique=True)

    # 시드 INSERT
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "INSERT INTO platform_specs (platform_name, default_aspect_ratio, default_resolution, default_duration_sec) "
            "VALUES (:platform_name, :default_aspect_ratio, :default_resolution, :default_duration_sec) "
            "ON CONFLICT (platform_name) DO NOTHING"
        ),
        _PLATFORM_SEED,
    )

    # ── 3. style_tags 테이블 생성 ─────────────────────────────────────────────
    op.create_table(
        "style_tags",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("tag_name", sa.String(100), unique=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ── 4. workspace_style_tags 조인 테이블 생성 ──────────────────────────────
    op.create_table(
        "workspace_style_tags",
        sa.Column("workspace_id", sa.BigInteger(), nullable=False),
        sa.Column("style_tag_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["workspace_id"], ["studio_workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["style_tag_id"], ["style_tags.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("workspace_id", "style_tag_id"),
        sa.UniqueConstraint("workspace_id", "style_tag_id", name="uq_workspace_style_tag"),
    )

    # ── 5. genres 테이블 생성 ─────────────────────────────────────────────────
    op.create_table(
        "genres",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("genre_name", sa.String(100), unique=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ── 6. gallery_item_genres 조인 테이블 생성 ───────────────────────────────
    op.create_table(
        "gallery_item_genres",
        sa.Column("gallery_item_id", sa.BigInteger(), nullable=False),
        sa.Column("genre_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["gallery_item_id"], ["gallery_items.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["genre_id"], ["genres.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("gallery_item_id", "genre_id"),
        sa.UniqueConstraint("gallery_item_id", "genre_id", name="uq_gallery_item_genre"),
    )

    # ── 7. users 테이블 변경 ──────────────────────────────────────────────────
    # role 컬럼 DROP (user_role ENUM 타입도 제거)
    op.drop_column("users", "role")
    op.execute("DROP TYPE IF EXISTS user_role")

    # deleted_at ADD
    op.add_column(
        "users",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # ── 8. studio_workspaces 테이블 변경 ─────────────────────────────────────
    # user_id FK 추가
    op.add_column(
        "studio_workspaces",
        sa.Column("user_id", sa.BigInteger(), nullable=True),
    )
    op.create_foreign_key(
        "fk_studio_workspaces_user_id",
        "studio_workspaces",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_studio_workspaces_user_id", "studio_workspaces", ["user_id"])

    # 신규 컬럼 추가 (존재하면 skip — IF NOT EXISTS)
    op.add_column(
        "studio_workspaces",
        sa.Column("neon_palette", sa.String(100), nullable=True),
    )
    op.add_column(
        "studio_workspaces",
        sa.Column("fragmentation_level", sa.Integer(), nullable=True),
    )
    op.add_column(
        "studio_workspaces",
        sa.Column("aspect_ratio", sa.String(10), nullable=True),
    )

    # custom_style_tags 컬럼 DROP (존재하는 경우만)
    conn2 = op.get_bind()
    result = conn2.execute(
        sa.text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'studio_workspaces' AND column_name = 'custom_style_tags'"
        )
    )
    if result.fetchone():
        op.drop_column("studio_workspaces", "custom_style_tags")

    # ── 9. gallery_items 테이블 변경 ─────────────────────────────────────────
    # genre_tags DROP
    result2 = conn2.execute(
        sa.text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'gallery_items' AND column_name = 'genre_tags'"
        )
    )
    if result2.fetchone():
        op.drop_column("gallery_items", "genre_tags")

    # created_by FK DROP (users 참조) → admins 참조로 변경
    _drop_fk_if_exists(conn2, "gallery_items", "users", "created_by")
    op.add_column(
        "gallery_items",
        sa.Column("created_by", sa.BigInteger(), nullable=True),
    )
    op.create_foreign_key(
        "fk_gallery_items_created_by_admins",
        "gallery_items",
        "admins",
        ["created_by"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_gallery_items_created_by", "gallery_items", ["created_by"])

    # ── 10. faq_entries — created_by → admins ────────────────────────────────
    _drop_fk_if_exists(conn2, "faq_entries", "users", "created_by")
    _add_created_by_fk(conn2, "faq_entries")

    # ── 11. magazine_articles — created_by → admins ──────────────────────────
    _drop_fk_if_exists(conn2, "magazine_articles", "users", "created_by")
    _add_created_by_fk(conn2, "magazine_articles")

    # ── 12. studio_analytics — created_by → admins ───────────────────────────
    _drop_fk_if_exists(conn2, "studio_analytics", "users", "created_by")
    _add_created_by_fk(conn2, "studio_analytics")


def downgrade() -> None:
    # ── 역순으로 복구 ─────────────────────────────────────────────────────────

    # 12~10. created_by FK 원복 (admins → 컬럼 DROP)
    for tbl in ("studio_analytics", "magazine_articles", "faq_entries"):
        op.drop_index(f"ix_{tbl}_created_by", table_name=tbl)
        op.drop_constraint(f"fk_{tbl}_created_by_admins", tbl, type_="foreignkey")
        op.drop_column(tbl, "created_by")

    # 9. gallery_items 원복
    op.drop_index("ix_gallery_items_created_by", table_name="gallery_items")
    op.drop_constraint("fk_gallery_items_created_by_admins", "gallery_items", type_="foreignkey")
    op.drop_column("gallery_items", "created_by")
    op.add_column(
        "gallery_items",
        sa.Column("genre_tags", sa.String(512), nullable=True),
    )

    # 8. studio_workspaces 원복
    op.drop_index("ix_studio_workspaces_user_id", table_name="studio_workspaces")
    op.drop_constraint("fk_studio_workspaces_user_id", "studio_workspaces", type_="foreignkey")
    op.drop_column("studio_workspaces", "user_id")
    op.drop_column("studio_workspaces", "neon_palette")
    op.drop_column("studio_workspaces", "fragmentation_level")
    op.drop_column("studio_workspaces", "aspect_ratio")

    # 7. users 원복
    op.drop_column("users", "deleted_at")
    op.execute(
        "DO $$ BEGIN "
        "  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN "
        "    CREATE TYPE user_role AS ENUM ('admin', 'user'); "
        "  END IF; "
        "END $$"
    )
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.Enum("admin", "user", name="user_role"),
            nullable=False,
            server_default="user",
        ),
    )

    # 6~1. 신규 테이블 DROP
    op.drop_table("gallery_item_genres")
    op.drop_table("genres")
    op.drop_table("workspace_style_tags")
    op.drop_table("style_tags")
    op.drop_index("ix_platform_specs_name", table_name="platform_specs")
    op.drop_table("platform_specs")
    op.drop_index("ix_admins_email", table_name="admins")
    op.drop_table("admins")


# ──────────────────────────────────────────────────────────────────────────────
# 헬퍼 함수
# ──────────────────────────────────────────────────────────────────────────────


def _drop_fk_if_exists(conn, table: str, ref_table: str, col: str) -> None:
    """특정 컬럼의 FK 제약이 있으면 DROP한다. 없으면 skip."""
    result = conn.execute(
        sa.text(
            "SELECT tc.constraint_name "
            "FROM information_schema.table_constraints tc "
            "JOIN information_schema.key_column_usage kcu "
            "  ON tc.constraint_name = kcu.constraint_name "
            "JOIN information_schema.referential_constraints rc "
            "  ON tc.constraint_name = rc.constraint_name "
            "JOIN information_schema.table_constraints tc2 "
            "  ON rc.unique_constraint_name = tc2.constraint_name "
            "WHERE tc.table_name = :table "
            "  AND kcu.column_name = :col "
            "  AND tc2.table_name = :ref_table "
            "  AND tc.constraint_type = 'FOREIGN KEY'"
        ),
        {"table": table, "col": col, "ref_table": ref_table},
    )
    row = result.fetchone()
    if row:
        op.drop_constraint(row[0], table, type_="foreignkey")


def _add_created_by_fk(conn, table: str) -> None:
    """created_by 컬럼이 없으면 ADD, FK → admins 생성."""
    exists = conn.execute(
        sa.text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = :table AND column_name = 'created_by'"
        ),
        {"table": table},
    ).fetchone()

    if not exists:
        op.add_column(table, sa.Column("created_by", sa.BigInteger(), nullable=True))

    op.create_foreign_key(
        f"fk_{table}_created_by_admins",
        table,
        "admins",
        ["created_by"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(f"ix_{table}_created_by", table, ["created_by"])
