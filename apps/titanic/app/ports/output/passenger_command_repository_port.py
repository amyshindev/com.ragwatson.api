from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.domain.entities.titanic import TitanicPassenger


class PassengerCommandRepositoryPort(Protocol):
    async def save(
        self,
        session: AsyncSession,
        passenger: TitanicPassenger,
    ) -> int:
        """승객을 저장하고 DB primary key(id)를 반환한다."""
