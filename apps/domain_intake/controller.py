"""도메인 폼 요청 단위 조립 및 로깅."""

import logging

from domain_intake.schemas import (
    DomainAcceptedResponse,
    FaqCreate,
    FaqEntryRead,
    GalleryCreate,
    GalleryItemRead,
    LibraryCreate,
    MagazineArticleRead,
    MagazineCreate,
    StudioAnalyticsCreate,
    StudioWorkspaceCreate,
)
from domain_intake.service import DomainIntakeService
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class DomainIntakeController:
    def __init__(self, svc: DomainIntakeService) -> None:
        self._svc = svc

    async def create_library(
        self,
        session: AsyncSession,
        body: LibraryCreate,
    ) -> DomainAcceptedResponse:
        result = await self._svc.create_library(session, body)
        logger.info("[DomainIntakeController] create_library 레이어 완료 — id=%s", result.id)
        return result

    async def create_studio_workspace(
        self,
        session: AsyncSession,
        body: StudioWorkspaceCreate,
    ) -> DomainAcceptedResponse:
        result = await self._svc.create_studio_workspace(session, body)
        logger.info(
            "[DomainIntakeController] create_studio_workspace 레이어 완료 — id=%s",
            result.id,
        )
        return result

    async def create_studio_analytics(
        self,
        session: AsyncSession,
        body: StudioAnalyticsCreate,
    ) -> DomainAcceptedResponse:
        result = await self._svc.create_studio_analytics(session, body)
        logger.info(
            "[DomainIntakeController] create_studio_analytics 레이어 완료 — id=%s",
            result.id,
        )
        return result

    async def create_gallery(
        self,
        session: AsyncSession,
        body: GalleryCreate,
        admin_user_id: int | None = None,
    ) -> DomainAcceptedResponse:
        result = await self._svc.create_gallery(session, body, admin_user_id)
        logger.info("[DomainIntakeController] create_gallery 레이어 완료 — id=%s", result.id)
        return result

    async def list_gallery(self, session: AsyncSession) -> list[GalleryItemRead]:
        return await self._svc.list_gallery(session)

    async def create_magazine(
        self,
        session: AsyncSession,
        body: MagazineCreate,
        admin_user_id: int | None = None,
    ) -> DomainAcceptedResponse:
        result = await self._svc.create_magazine(session, body, admin_user_id)
        logger.info("[DomainIntakeController] create_magazine 레이어 완료 — id=%s", result.id)
        return result

    async def list_magazine(self, session: AsyncSession) -> list[MagazineArticleRead]:
        return await self._svc.list_magazine(session)

    async def create_faq(
        self,
        session: AsyncSession,
        body: FaqCreate,
        admin_user_id: int | None = None,
    ) -> DomainAcceptedResponse:
        result = await self._svc.create_faq(session, body, admin_user_id)
        logger.info("[DomainIntakeController] create_faq 레이어 완료 — id=%s", result.id)
        return result

    async def list_faq(self, session: AsyncSession) -> list[FaqEntryRead]:
        return await self._svc.list_faq(session)
