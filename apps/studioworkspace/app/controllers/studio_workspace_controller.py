"""스튜디오 워크스페이스 (/studio/workspace): 세션 설정·생성 Job 큐."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from studioworkspace.app.services.studio_workspace_service import (
    StudioWorkspaceService,
)

logger = logging.getLogger(__name__)


class StudioWorkspaceController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = StudioWorkspaceService(session)
