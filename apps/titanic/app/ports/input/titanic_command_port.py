from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.domain.entities.titanic import TitanicPassenger


class TitanicCommandPort(Protocol):
    async def create_passenger(
        self,
        session: AsyncSession,
        passenger: TitanicPassenger,
    ) -> tuple[int, TitanicPassenger]:
        """승객을 저장하고 (db_id, entity)를 반환한다."""
