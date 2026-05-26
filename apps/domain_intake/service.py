"""도메인 폼 비즈니스 규칙·저장 호출."""

import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain_intake.repository import DomainIntakeRepositories
from domain_intake.schemas import (
    DomainAcceptedResponse,
    FaqCreate,
    FaqEntryRead,
    GalleryCreate,
    GalleryItemRead,
    LibraryCreate,
    MagazineCreate,
    MagazineArticleRead,
    StudioAnalyticsCreate,
    StudioWorkspaceCreate,
)
from secom.app.models.role import UserRole
from secom.app.models.user import User

logger = logging.getLogger(__name__)


class DomainIntakeService:
    def __init__(self, repos: DomainIntakeRepositories) -> None:
        self._repos = repos

    async def _require_admin(self, session: AsyncSession, user_id: int | None) -> None:
        if user_id is None:
            raise HTTPException(status_code=401, detail="관리자 로그인이 필요합니다.")

        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=401, detail="관리자 계정을 찾을 수 없습니다.")
        if user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="관리자 권한이 필요합니다.")

    async def create_library(
        self,
        session: AsyncSession,
        body: LibraryCreate,
    ) -> DomainAcceptedResponse:
        rid = await self._repos.library.create(session, body)
        logger.info("[DomainIntakeService] library 항목 id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="library.item")

    async def create_studio_workspace(
        self,
        session: AsyncSession,
        body: StudioWorkspaceCreate,
    ) -> DomainAcceptedResponse:
        rid = await self._repos.studio_workspace.create(session, body)
        logger.info("[DomainIntakeService] studio.workspace id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="studio.workspace")

    async def create_studio_analytics(
        self,
        session: AsyncSession,
        body: StudioAnalyticsCreate,
    ) -> DomainAcceptedResponse:
        rid = await self._repos.studio_analytics.create(session, body)
        logger.info("[DomainIntakeService] studio.analytics id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="studio.analytics")

    async def create_gallery(
        self,
        session: AsyncSession,
        body: GalleryCreate,
        admin_user_id: int | None = None,
    ) -> DomainAcceptedResponse:
        await self._require_admin(session, admin_user_id)
        rid = await self._repos.gallery.create(session, body)
        logger.info("[DomainIntakeService] gallery.item id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="gallery.item")

    async def list_gallery(self, session: AsyncSession) -> list[GalleryItemRead]:
        rows = await self._repos.gallery.list(session)
        return [
            GalleryItemRead(
                id=row.id,
                workTitle=row.work_title,
                artist=row.artist,
                genreTags=row.genre_tags,
                mediaUrl=row.media_url,
                createdAt=row.created_at,
            )
            for row in rows
        ]

    async def create_magazine(
        self,
        session: AsyncSession,
        body: MagazineCreate,
        admin_user_id: int | None = None,
    ) -> DomainAcceptedResponse:
        await self._require_admin(session, admin_user_id)
        rid = await self._repos.magazine.create(session, body)
        logger.info("[DomainIntakeService] magazine.article id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="magazine.article")

    async def list_magazine(self, session: AsyncSession) -> list[MagazineArticleRead]:
        rows = await self._repos.magazine.list(session)
        return [
            MagazineArticleRead(
                id=row.id,
                articleTitle=row.article_title,
                author=row.author,
                excerpt=row.excerpt,
                body=row.body,
                createdAt=row.created_at,
            )
            for row in rows
        ]

    async def create_faq(
        self,
        session: AsyncSession,
        body: FaqCreate,
        admin_user_id: int | None = None,
    ) -> DomainAcceptedResponse:
        await self._require_admin(session, admin_user_id)
        rid = await self._repos.faq.create(session, body)
        logger.info("[DomainIntakeService] faq.entry id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="faq.entry")

    async def list_faq(self, session: AsyncSession) -> list[FaqEntryRead]:
        rows = await self._repos.faq.list(session)
        return [
            FaqEntryRead(
                id=row.id,
                category=row.category,
                question=row.question,
                answer=row.answer,
                createdAt=row.created_at,
            )
            for row in rows
        ]
