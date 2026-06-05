from __future__ import annotations

import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from user.adapter.outbound.orm.user_model import UserRecord
from user.adapter.outbound.pg.password_hasher import verify_password
from user.app.ports.output.login_repository import LoginRepository
from user.domain.entities.user import User

log = logging.getLogger(__name__)


def _to_domain(row: UserRecord) -> User:
    return User(
        id=row.id,
        email=row.email,
        username=row.username,
        nickname=row.nickname,
        # role 제거 — v4: User 엔티티에 role 없음
    )


class LoginPgRepository(LoginRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def login(self, email: str, plain_password: str) -> User:
        normalized_email = email.strip().lower()
        result = await self._session.execute(
            select(UserRecord).where(UserRecord.email == normalized_email)
        )
        row = result.scalar_one_or_none()
        if row is None or not verify_password(plain_password, row.password):
            raise HTTPException(
                status_code=401,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )
        user = _to_domain(row)
        log.info("[LoginPgRepository] login 완료 — id=%s", user.id)
        return user
