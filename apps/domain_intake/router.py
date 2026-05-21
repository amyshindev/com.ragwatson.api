"""POST /api/domain/* — 폼 연동 (도메인별 PostgreSQL 테이블)."""

import logging
from collections.abc import Awaitable, Callable

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain_intake.controller import DomainIntakeController
from domain_intake.repository import DomainIntakeRepositories
from domain_intake.service import DomainIntakeService
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
from db.session import DbSession

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/domain", tags=["domain-intake"])

_repos = DomainIntakeRepositories()
_svc = DomainIntakeService(_repos)
_ctrl = DomainIntakeController(_svc)


async def _with_commit(
    session: AsyncSession,
    work: Callable[[], Awaitable[DomainAcceptedResponse]],
) -> DomainAcceptedResponse:
    try:
        result = await work()
        await session.commit()
        return result
    except HTTPException:
        await session.rollback()
        raise
    except Exception as exc:
        await session.rollback()
        log.exception("domain intake transaction failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/library", response_model=DomainAcceptedResponse)
async def post_library(
    body: LibraryCreate,
    session: DbSession,
) -> DomainAcceptedResponse:
    return await _with_commit(session, lambda: _ctrl.create_library(session, body))


studio_router = APIRouter(prefix="/studio")


@studio_router.post("/workspace", response_model=DomainAcceptedResponse)
async def post_studio_workspace(
    body: StudioWorkspaceCreate,
    session: DbSession,
) -> DomainAcceptedResponse:
    return await _with_commit(session, lambda: _ctrl.create_studio_workspace(session, body))


@studio_router.post("/analytics", response_model=DomainAcceptedResponse)
async def post_studio_analytics(
    body: StudioAnalyticsCreate,
    session: DbSession,
) -> DomainAcceptedResponse:
    return await _with_commit(session, lambda: _ctrl.create_studio_analytics(session, body))


router.include_router(studio_router)


@router.post("/membership/inquiry", response_model=DomainAcceptedResponse)
async def post_membership_inquiry(
    body: MembershipInquiryCreate,
    session: DbSession,
) -> DomainAcceptedResponse:
    return await _with_commit(session, lambda: _ctrl.create_membership_inquiry(session, body))


@router.post("/gallery", response_model=DomainAcceptedResponse)
async def post_gallery(
    body: GalleryCreate,
    session: DbSession,
) -> DomainAcceptedResponse:
    return await _with_commit(session, lambda: _ctrl.create_gallery(session, body))


@router.post("/magazine", response_model=DomainAcceptedResponse)
async def post_magazine(
    body: MagazineCreate,
    session: DbSession,
) -> DomainAcceptedResponse:
    return await _with_commit(session, lambda: _ctrl.create_magazine(session, body))


@router.post("/faq", response_model=DomainAcceptedResponse)
async def post_faq(
    body: FaqCreate,
    session: DbSession,
) -> DomainAcceptedResponse:
    return await _with_commit(session, lambda: _ctrl.create_faq(session, body))
