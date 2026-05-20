"""워크스페이스 영속화."""

from sqlalchemy.ext.asyncio import AsyncSession


class StudioWorkspaceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
