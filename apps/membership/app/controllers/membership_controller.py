"""멤버십·구독 (/pricing, billing): 플랜·상태·결제 메타(PG 연동 전제)."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from membership.app.services.membership_service import MembershipService

logger = logging.getLogger(__name__)


class MembershipController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = MembershipService(session)
