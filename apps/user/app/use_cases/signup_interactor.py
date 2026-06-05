from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from user.adapter.inbound.api.schemas import SignupRequest, SignupResponse, UserResponse
from user.app.ports.input.signup_use_case import SignupUseCase
from user.app.ports.output.signup_repository import SignupRepository

log = logging.getLogger(__name__)


class SignupInteractor(SignupUseCase):
    def __init__(self, session: AsyncSession, repository: SignupRepository) -> None:
        self._session = session
        self._repository = repository

    async def signup(self, req: SignupRequest) -> SignupResponse:
        log.info("[SignupInteractor] signup 시작 — email=%s", req.email)
        user = req.to_entity()
        try:
            saved = await self._repository.signup(user, req.password)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise

        log.info("[SignupInteractor] signup 완료 — userId=%s", saved.id)
        return SignupResponse(user=UserResponse.from_entity(saved))
