"""매거진 비즈니스 로직."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from magazine.app.repositories.magazine_repository import MagazineRepository

logger = logging.getLogger(__name__)


class MagazineService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = MagazineRepository(session)
