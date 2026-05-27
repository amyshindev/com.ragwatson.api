from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.models.passenger import Passenger
from titanic.domain.entities.titanic import TitanicPassenger


def _optional_str(value: str) -> str | None:
    return value if value else None


def _optional_float(value: str) -> float | None:
    if not value:
        return None
    return float(value)


class PassengerCommandRepository:
    async def save(self, session: AsyncSession, passenger: TitanicPassenger) -> int:
        row = Passenger(
            passenger_id=int(passenger.passenger_id),
            survived=int(passenger.survived),
            pclass=int(passenger.pclass),
            name=passenger.name,
            sex=passenger.gender,
            age=_optional_float(passenger.age),
            sibsp=int(passenger.sibsp),
            parch=int(passenger.parch),
            ticket=passenger.ticket,
            fare=float(passenger.fare),
            cabin=_optional_str(passenger.cabin),
            embarked=_optional_str(passenger.embarked),
        )
        session.add(row)
        await session.flush()
        return int(row.id)
