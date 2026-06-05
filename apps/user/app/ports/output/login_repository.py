from __future__ import annotations

from abc import ABC, abstractmethod

from friday13th.domain.entities.user import User


class LoginRepository(ABC):
    @abstractmethod
    async def login(self, email: str, plain_password: str) -> User:
        """이메일·비밀번호로 인증 후 도메인 User를 반환한다."""
