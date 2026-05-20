"""구독·결제 영속화."""

from sqlalchemy.ext.asyncio import AsyncSession


class MembershipRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
