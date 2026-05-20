"""마이 아카이브 영속화."""

from sqlalchemy.ext.asyncio import AsyncSession


class LibraryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
