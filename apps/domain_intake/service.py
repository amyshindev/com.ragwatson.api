"""도메인 폼 비즈니스 규칙·저장 호출."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from domain_intake.repository import DomainIntakeRepository
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

logger = logging.getLogger(__name__)


class DomainIntakeService:
    def __init__(self, repo: DomainIntakeRepository) -> None:
        self._repo = repo

    async def create_library(
        self,
        session: AsyncSession,
        body: LibraryCreate,
    ) -> DomainAcceptedResponse:
        rid = await self._repo.append(session, "library.item", body.model_dump(mode="json"))
        logger.info("[DomainIntakeService] library 항목 id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="library.item")

    async def create_studio_workspace(
        self,
        session: AsyncSession,
        body: StudioWorkspaceCreate,
    ) -> DomainAcceptedResponse:
        rid = await self._repo.append(session, "studio.workspace", body.model_dump(mode="json"))
        logger.info("[DomainIntakeService] studio.workspace id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="studio.workspace")

    async def create_studio_analytics(
        self,
        session: AsyncSession,
        body: StudioAnalyticsCreate,
    ) -> DomainAcceptedResponse:
        rid = await self._repo.append(session, "studio.analytics", body.model_dump(mode="json"))
        logger.info("[DomainIntakeService] studio.analytics id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="studio.analytics")

    async def create_membership_inquiry(
        self,
        session: AsyncSession,
        body: MembershipInquiryCreate,
    ) -> DomainAcceptedResponse:
        rid = await self._repo.append(
            session,
            "membership.inquiry",
            body.model_dump(mode="json"),
        )
        logger.info("[DomainIntakeService] membership.inquiry id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="membership.inquiry")

    async def create_gallery(
        self,
        session: AsyncSession,
        body: GalleryCreate,
    ) -> DomainAcceptedResponse:
        rid = await self._repo.append(session, "gallery.item", body.model_dump(mode="json"))
        logger.info("[DomainIntakeService] gallery.item id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="gallery.item")

    async def create_magazine(
        self,
        session: AsyncSession,
        body: MagazineCreate,
    ) -> DomainAcceptedResponse:
        rid = await self._repo.append(session, "magazine.article", body.model_dump(mode="json"))
        logger.info("[DomainIntakeService] magazine.article id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="magazine.article")

    async def create_faq(
        self,
        session: AsyncSession,
        body: FaqCreate,
    ) -> DomainAcceptedResponse:
        rid = await self._repo.append(session, "faq.entry", body.model_dump(mode="json"))
        logger.info("[DomainIntakeService] faq.entry id=%s", rid)
        return DomainAcceptedResponse(id=rid, kind="faq.entry")
