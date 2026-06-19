from __future__ import annotations

import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from user.adapter.outbound.orm.admin_model import AdminRecord
from user.adapter.outbound.pg.password_hasher import verify_password
from user.domain.entities.admin import Admin

log = logging.getLogger(__name__)


def _to_domain(row: AdminRecord) -> Admin:
    return Admin(
        id=row.id,
        email=row.email,
        username=row.username,
    )


class AdminLoginPgRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def login(self, email: str, plain_password: str) -> Admin:
        normalized_email = email.strip().lower()
        result = await self._session.execute(
            select(AdminRecord).where(
                AdminRecord.email == normalized_email,
                AdminRecord.deleted_at.is_(None),
            )
        )
        row = result.scalar_one_or_none()
        if row is None or not verify_password(plain_password, row.password):
            raise HTTPException(
                status_code=401,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )
        admin = _to_domain(row)
        log.info("[AdminLoginPgRepository] login 완료 — id=%s", admin.id)
        return admin
