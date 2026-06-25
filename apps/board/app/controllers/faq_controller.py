"""FAQ (/faq): 질문·답변·카테고리·순서·노출."""

import logging

from board.app.services.faq_service import FaqService
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class FaqController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = FaqService(session)
