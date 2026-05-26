"""POST /api/domain/* — 폼 연동 (도메인별 PostgreSQL 테이블)."""

import logging
from typing import Annotated
from collections.abc import Awaitable, Callable

from fastapi import APIRouter, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain_intake.controller import DomainIntakeController
from domain_intake.repository import DomainIntakeRepositories
from domain_intake.service import DomainIntakeService
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
from db.session import DbSession

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/domain", tags=["domain-intake"])

_repos = DomainIntakeRepositories()
_svc = DomainIntakeService(_repos)
_ctrl = DomainIntakeController(_svc)

AdminUserIdHeader = Annotated[int | None, Header(alias="X-Maestro-User-Id")]


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


@router.post("/gallery", response_model=DomainAcceptedResponse)
async def post_gallery(
    body: GalleryCreate,
    session: DbSession,
    admin_user_id: AdminUserIdHeader = None,
) -> DomainAcceptedResponse:
    return await _with_commit(
        session,
        lambda: _ctrl.create_gallery(session, body, admin_user_id),
    )


@router.get("/gallery", response_model=list[GalleryItemRead])
async def get_gallery(session: DbSession) -> list[GalleryItemRead]:
    return await _ctrl.list_gallery(session)


@router.post("/magazine", response_model=DomainAcceptedResponse)
async def post_magazine(
    body: MagazineCreate,
    session: DbSession,
    admin_user_id: AdminUserIdHeader = None,
) -> DomainAcceptedResponse:
    return await _with_commit(
        session,
        lambda: _ctrl.create_magazine(session, body, admin_user_id),
    )


@router.get("/magazine", response_model=list[MagazineArticleRead])
async def get_magazine(session: DbSession) -> list[MagazineArticleRead]:
    return await _ctrl.list_magazine(session)


@router.post("/faq", response_model=DomainAcceptedResponse)
async def post_faq(
    body: FaqCreate,
    session: DbSession,
    admin_user_id: AdminUserIdHeader = None,
) -> DomainAcceptedResponse:
    return await _with_commit(
        session,
        lambda: _ctrl.create_faq(session, body, admin_user_id),
    )


@router.get("/faq", response_model=list[FaqEntryRead])
async def get_faq(session: DbSession) -> list[FaqEntryRead]:
    return await _ctrl.list_faq(session)
