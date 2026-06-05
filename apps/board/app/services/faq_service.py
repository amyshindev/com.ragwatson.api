"""FAQ 비즈니스 로직."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from board.app.repositories.faq_repository import FaqRepository

logger = logging.getLogger(__name__)


class FaqService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = FaqRepository(session)
