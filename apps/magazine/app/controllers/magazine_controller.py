"""매거진 (/magazine): 기사·썸네일·발행 상태."""

import logging

from magazine.app.services.magazine_service import MagazineService
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class MagazineController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = MagazineService(session)
