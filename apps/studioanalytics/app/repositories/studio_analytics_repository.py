"""분석 결과 영속화."""

from sqlalchemy.ext.asyncio import AsyncSession


class StudioAnalyticsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
