from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from user.adapter.inbound.api.schemas.admin_schema import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminSessionUser,
)
from user.adapter.outbound.pg.admin_login_pg_repository import AdminLoginPgRepository

log = logging.getLogger(__name__)


class AdminLoginInteractor:
    def __init__(self, session: AsyncSession, repository: AdminLoginPgRepository) -> None:
        self._session = session
        self._repository = repository

    async def login(self, req: AdminLoginRequest) -> AdminLoginResponse:
        log.info("[AdminLoginInteractor] login 시작 — email=%s", req.email)
        try:
            admin = await self._repository.login(str(req.email), req.password)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise

        if admin.id is None:
            raise ValueError("Admin id is required for API response")

        log.info("[AdminLoginInteractor] login 완료 — id=%s", admin.id)
        return AdminLoginResponse(
            user=AdminSessionUser(
                id=admin.id,
                email=admin.email,
                username=admin.username,
                nickname=admin.username,
                role="admin",
            )
        )
