from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.models.role import UserRole
from secom.app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
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
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> User | None:
        r = await self._session.execute(
            select(User).where(User.email == email.strip().lower())
        )
        return r.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        r = await self._session.execute(
            select(User).where(User.username == username.strip())
        )
        return r.scalar_one_or_none()

    async def count(self) -> int:
        r = await self._session.execute(select(func.count()).select_from(User))
        return int(r.scalar_one())
