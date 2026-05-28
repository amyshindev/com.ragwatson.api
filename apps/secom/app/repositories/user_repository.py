import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.models.role import UserRole
from secom.app.models.user import User

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_user(
        self,
        *,
        email: str,
        username: str,
        nickname: str,
        password: str,
        role: UserRole,
    ) -> User:
        user = User(
            email=email.strip().lower(),
            username=username.strip(),
            nickname=nickname.strip(),
            password=password,
            role=role,
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        logger.info("[UserRepository] save_user 레이어 완료 — id=%s", user.id)
        return user

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email.strip().lower())
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username.strip())
        )
        return result.scalar_one_or_none()

