"""멤버십·구독 비즈니스 로직."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from membership.app.repositories.membership_repository import MembershipRepository

logger = logging.getLogger(__name__)


class MembershipService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = MembershipRepository(session)
