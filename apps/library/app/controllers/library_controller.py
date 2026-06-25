"""마이 아카이브 (/library): 업로드·프로젝트·비주얼 메타·렌더 상태."""

import logging

from library.app.services.library_service import LibraryService
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class LibraryController:
    def __init__(self, session: AsyncSession) -> None:
        self._library_service = LibraryService(session)
