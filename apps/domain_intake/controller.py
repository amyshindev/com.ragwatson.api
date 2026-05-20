"""도메인 폼 요청 단위 조립 및 로깅."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from domain_intake.schemas import (
    DomainAcceptedResponse,
    FaqCreate,
    GalleryCreate,
    LibraryCreate,
    MagazineCreate,
    MembershipInquiryCreate,
    StudioAnalyticsCreate,
    StudioWorkspaceCreate,
)
from domain_intake.service import DomainIntakeService

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

    async def create_membership_inquiry(
        self,
        session: AsyncSession,
        body: MembershipInquiryCreate,
    ) -> DomainAcceptedResponse:
        result = await self._svc.create_membership_inquiry(session, body)
        logger.info(
            "[DomainIntakeController] create_membership_inquiry 레이어 완료 — id=%s",
            result.id,
        )
        return result

    async def create_gallery(
        self,
        session: AsyncSession,
        body: GalleryCreate,
    ) -> DomainAcceptedResponse:
        result = await self._svc.create_gallery(session, body)
        logger.info("[DomainIntakeController] create_gallery 레이어 완료 — id=%s", result.id)
        return result

    async def create_magazine(
        self,
        session: AsyncSession,
        body: MagazineCreate,
    ) -> DomainAcceptedResponse:
        result = await self._svc.create_magazine(session, body)
        logger.info("[DomainIntakeController] create_magazine 레이어 완료 — id=%s", result.id)
        return result

    async def create_faq(
        self,
        session: AsyncSession,
        body: FaqCreate,
    ) -> DomainAcceptedResponse:
        result = await self._svc.create_faq(session, body)
        logger.info("[DomainIntakeController] create_faq 레이어 완료 — id=%s", result.id)
        return result
