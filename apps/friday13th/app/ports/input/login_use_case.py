from __future__ import annotations

from abc import ABC, abstractmethod

from friday13th.adapter.inbound.api.schemas import LoginRequest, LoginResponse


class LoginUseCase(ABC):
    @abstractmethod
    async def login(self, req: LoginRequest) -> LoginResponse:
        ...
