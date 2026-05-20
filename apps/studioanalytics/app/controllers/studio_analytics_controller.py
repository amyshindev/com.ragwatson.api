"""오디오 분석 대시보드 (/studio/analytics): BPM·무드·장르·파형 메타."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from studioanalytics.app.services.studio_analytics_service import (
    StudioAnalyticsService,
)

logger = logging.getLogger(__name__)


class StudioAnalyticsController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = StudioAnalyticsService(session)
