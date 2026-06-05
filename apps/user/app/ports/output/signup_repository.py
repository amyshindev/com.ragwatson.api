from __future__ import annotations

from abc import ABC, abstractmethod

from friday13th.domain.entities.user import User


class SignupRepository(ABC):
    @abstractmethod
    async def signup(self, user: User, plain_password: str) -> User:
        """회원을 저장하고 id가 채워진 도메인 User를 반환한다."""
