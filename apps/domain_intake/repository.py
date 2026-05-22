"""도메인별 테이블 영속화."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from domain_intake.models.faq_entry import FaqEntry
from domain_intake.models.gallery_item import GalleryItem
from domain_intake.models.library_item import LibraryItem
from domain_intake.models.magazine_article import MagazineArticle
from domain_intake.models.studio_analytics import StudioAnalytics
from domain_intake.models.studio_workspace import StudioWorkspace
from domain_intake.schemas import (
    FaqCreate,
    GalleryCreate,
    LibraryCreate,
    MagazineCreate,
    StudioAnalyticsCreate,
    StudioWorkspaceCreate,
)

logger = logging.getLogger(__name__)


async def _flush_id(session: AsyncSession, row: object) -> int:
    await session.flush()
    rid = getattr(row, "id", None)
    assert isinstance(rid, int)
    return rid


class LibraryRepository:
    async def create(self, session: AsyncSession, body: LibraryCreate) -> int:
        row = LibraryItem(
            project_title=body.projectTitle,
            memo=body.memo,
            tags=body.tags,
        )
        session.add(row)
        rid = await _flush_id(session, row)
        logger.info("[LibraryRepository] create id=%s", rid)
        return rid


class StudioWorkspaceRepository:
    async def create(self, session: AsyncSession, body: StudioWorkspaceCreate) -> int:
        row = StudioWorkspace(
            workspace_name=body.workspaceName,
            glitch_intensity=body.glitchIntensity,
            notes=body.notes,
        )
        session.add(row)
        rid = await _flush_id(session, row)
        logger.info("[StudioWorkspaceRepository] create id=%s", rid)
        return rid


class StudioAnalyticsRepository:
    async def create(self, session: AsyncSession, body: StudioAnalyticsCreate) -> int:
        row = StudioAnalytics(
            track_title=body.trackTitle,
            bpm=body.bpm,
            mood=body.mood,
            genre=body.genre,
        )
        session.add(row)
        rid = await _flush_id(session, row)
        logger.info("[StudioAnalyticsRepository] create id=%s", rid)
        return rid


class GalleryRepository:
    async def create(self, session: AsyncSession, body: GalleryCreate) -> int:
        row = GalleryItem(
            work_title=body.workTitle,
            artist=body.artist,
            genre_tags=body.genreTags,
            media_url=body.mediaUrl,
        )
        session.add(row)
        rid = await _flush_id(session, row)
        logger.info("[GalleryRepository] create id=%s", rid)
        return rid


class MagazineRepository:
    async def create(self, session: AsyncSession, body: MagazineCreate) -> int:
        row = MagazineArticle(
            article_title=body.articleTitle,
            author=body.author,
            excerpt=body.excerpt,
            body=body.body,
        )
        session.add(row)
        rid = await _flush_id(session, row)
        logger.info("[MagazineRepository] create id=%s", rid)
        return rid


class FaqRepository:
    async def create(self, session: AsyncSession, body: FaqCreate) -> int:
        row = FaqEntry(
            category=body.category,
            question=body.question,
            answer=body.answer,
        )
        session.add(row)
        rid = await _flush_id(session, row)
        logger.info("[FaqRepository] create id=%s", rid)
        return rid


class DomainIntakeRepositories:
    def __init__(self) -> None:
        self.library = LibraryRepository()
        self.studio_workspace = StudioWorkspaceRepository()
        self.studio_analytics = StudioAnalyticsRepository()
        self.gallery = GalleryRepository()
        self.magazine = MagazineRepository()
        self.faq = FaqRepository()
