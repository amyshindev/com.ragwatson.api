"""마이 아카이브 비즈니스 로직."""

import logging

from library.app.repositories.library_repository import LibraryRepository
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class LibraryService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = LibraryRepository(session)
