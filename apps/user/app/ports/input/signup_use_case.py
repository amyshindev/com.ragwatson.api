from __future__ import annotations

from abc import ABC, abstractmethod

from user.adapter.inbound.api.schemas import SignupRequest, SignupResponse


class SignupUseCase(ABC):
    @abstractmethod
    async def signup(self, req: SignupRequest) -> SignupResponse:
        ...
