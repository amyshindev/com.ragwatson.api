from __future__ import annotations

import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from friday13th.adapter.outbound.orm.friday13th_model import UserRecord
from friday13th.adapter.outbound.pg.password_hasher import hash_password
from friday13th.app.ports.output.signup_repository import SignupRepository
from friday13th.domain.entities.user import User

log = logging.getLogger(__name__)


def _to_domain(row: UserRecord) -> User:
    return User(
        id=row.id,
        email=row.email,
        username=row.username,
        nickname=row.nickname,
        role=row.role,
    )


class SignupPgRepository(SignupRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def signup(self, user: User, plain_password: str) -> User:
        email_result = await self._session.execute(
            select(UserRecord).where(UserRecord.email == user.email)
        )
        if email_result.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="이미 사용 중인 이메일입니다.")

        username_result = await self._session.execute(
            select(UserRecord).where(UserRecord.username == user.username)
        )
        if username_result.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다.")

        row = UserRecord(
            email=user.email,
            username=user.username,
            nickname=user.nickname,
            password=hash_password(plain_password),
            role=user.role,
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        saved = _to_domain(row)
        log.info("[SignupPgRepository] signup 완료 — id=%s", saved.id)
        return saved
