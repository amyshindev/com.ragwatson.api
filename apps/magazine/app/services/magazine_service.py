"""매거진 비즈니스 로직."""

import logging

from magazine.app.repositories.magazine_repository import MagazineRepository
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class MagazineService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = MagazineRepository(session)
