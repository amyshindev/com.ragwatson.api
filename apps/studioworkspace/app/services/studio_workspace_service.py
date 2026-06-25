"""워크스페이스 비즈니스 로직."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession
from studioworkspace.app.repositories.studio_workspace_repository import (
    StudioWorkspaceRepository,
)

logger = logging.getLogger(__name__)


class StudioWorkspaceService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = StudioWorkspaceRepository(session)
