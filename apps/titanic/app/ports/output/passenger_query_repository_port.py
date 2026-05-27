from typing import Any, Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class PassengerQueryRepositoryPort(Protocol):
    async def find_first_records(self, session: AsyncSession) -> list[dict[str, Any]]:
        """첫 번째 승객 레코드를 dict 목록으로 반환한다."""

    async def count_passengers(self, session: AsyncSession) -> int:
        """승객 수를 반환한다."""
