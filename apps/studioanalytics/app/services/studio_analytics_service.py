"""오디오 분석 비즈니스 로직."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from studioanalytics.app.repositories.studio_analytics_repository import (
    StudioAnalyticsRepository,
)

logger = logging.getLogger(__name__)


class StudioAnalyticsService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = StudioAnalyticsRepository(session)
