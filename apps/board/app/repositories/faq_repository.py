"""FAQ 영속화."""

from sqlalchemy.ext.asyncio import AsyncSession


class FaqRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
