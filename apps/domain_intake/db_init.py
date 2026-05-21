"""레거시 domain_intake_records → 도메인별 테이블 1회 이전."""

import logging

from sqlalchemy import text

log = logging.getLogger(__name__)

_MIGRATION_STATEMENTS: tuple[str, ...] = (
    """
    INSERT INTO library_items (project_title, memo, tags, created_at)
    SELECT
      COALESCE(r.payload->>'projectTitle', ''),
      NULLIF(r.payload->>'memo', ''),
      NULLIF(r.payload->>'tags', ''),
      r.created_at
    FROM domain_intake_records r
    WHERE r.kind = 'library.item'
      AND NOT EXISTS (SELECT 1 FROM library_items LIMIT 1)
    """,
    """
    INSERT INTO studio_workspaces (workspace_name, glitch_intensity, notes, created_at)
    SELECT
      COALESCE(r.payload->>'workspaceName', ''),
      COALESCE((r.payload->>'glitchIntensity')::int, 42),
      NULLIF(r.payload->>'notes', ''),
      r.created_at
    FROM domain_intake_records r
    WHERE r.kind = 'studio.workspace'
      AND NOT EXISTS (SELECT 1 FROM studio_workspaces LIMIT 1)
    """,
    """
    INSERT INTO studio_analytics (track_title, bpm, mood, genre, created_at)
    SELECT
      COALESCE(r.payload->>'trackTitle', ''),
      NULLIF(r.payload->>'bpm', '')::int,
      NULLIF(r.payload->>'mood', ''),
      NULLIF(r.payload->>'genre', ''),
      r.created_at
    FROM domain_intake_records r
    WHERE r.kind = 'studio.analytics'
      AND NOT EXISTS (SELECT 1 FROM studio_analytics LIMIT 1)
    """,
    """
    INSERT INTO membership_inquiries (email, plan, message, created_at)
    SELECT
      COALESCE(r.payload->>'email', ''),
      COALESCE(r.payload->>'plan', 'free'),
      NULLIF(r.payload->>'message', ''),
      r.created_at
    FROM domain_intake_records r
    WHERE r.kind = 'membership.inquiry'
      AND NOT EXISTS (SELECT 1 FROM membership_inquiries LIMIT 1)
    """,
    """
    INSERT INTO gallery_items (work_title, artist, genre_tags, media_url, created_at)
    SELECT
      COALESCE(r.payload->>'workTitle', ''),
      COALESCE(r.payload->>'artist', ''),
      NULLIF(r.payload->>'genreTags', ''),
      NULLIF(r.payload->>'mediaUrl', ''),
      r.created_at
    FROM domain_intake_records r
    WHERE r.kind = 'gallery.item'
      AND NOT EXISTS (SELECT 1 FROM gallery_items LIMIT 1)
    """,
    """
    INSERT INTO magazine_articles (article_title, author, excerpt, body, created_at)
    SELECT
      COALESCE(r.payload->>'articleTitle', ''),
      COALESCE(r.payload->>'author', ''),
      NULLIF(r.payload->>'excerpt', ''),
      NULLIF(r.payload->>'body', ''),
      r.created_at
    FROM domain_intake_records r
    WHERE r.kind = 'magazine.article'
      AND NOT EXISTS (SELECT 1 FROM magazine_articles LIMIT 1)
    """,
    """
    INSERT INTO faq_entries (category, question, answer, created_at)
    SELECT
      NULLIF(r.payload->>'category', ''),
      COALESCE(r.payload->>'question', ''),
      COALESCE(r.payload->>'answer', ''),
      r.created_at
    FROM domain_intake_records r
    WHERE r.kind = 'faq.entry'
      AND NOT EXISTS (SELECT 1 FROM faq_entries LIMIT 1)
    """,
)


async def migrate_legacy_domain_intake_records(conn) -> None:
    exists = await conn.execute(
        text(
            """
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = current_schema()
              AND table_name = 'domain_intake_records'
            """
        )
    )
    if exists.first() is None:
        return

    for stmt in _MIGRATION_STATEMENTS:
        await conn.execute(text(stmt))
    log.info("domain_intake_records → per-domain tables migration attempted (if legacy had rows)")
