from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from user.adapter.inbound.api.schemas import LoginRequest, LoginResponse, UserResponse
from user.app.ports.input.login_use_case import LoginUseCase
from user.app.ports.output.login_repository import LoginRepository

log = logging.getLogger(__name__)


class LoginInteractor(LoginUseCase):
    def __init__(self, session: AsyncSession, repository: LoginRepository) -> None:
        self._session = session
        self._repository = repository

    async def login(self, req: LoginRequest) -> LoginResponse:
        log.info("[LoginInteractor] login 시작 — email=%s", req.email)
        try:
            user = await self._repository.login(str(req.email), req.password)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise

        log.info("[LoginInteractor] login 완료 — id=%s", user.id)
        return LoginResponse(user=UserResponse.from_entity(user))
