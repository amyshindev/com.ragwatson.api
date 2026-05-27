from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.models.passenger import Passenger


class PassengerQueryRepository:
    async def find_first_records(self, session: AsyncSession) -> list[dict[str, Any]]:
        result = await session.execute(
            select(Passenger).order_by(Passenger.passenger_id).limit(1)
        )
        passenger = result.scalar_one_or_none()
        if passenger is None:
            return []

        return [
            {
                "PassengerId": passenger.passenger_id,
                "Survived": passenger.survived,
                "Pclass": passenger.pclass,
                "Name": passenger.name,
                "Sex": passenger.sex,
                "Age": passenger.age,
                "SibSp": passenger.sibsp,
                "Parch": passenger.parch,
                "Ticket": passenger.ticket,
                "Fare": passenger.fare,
                "Cabin": passenger.cabin,
                "Boat": passenger.boat,
                "Embarked": passenger.embarked,
            }
        ]

    async def count_passengers(self, session: AsyncSession) -> int:
        result = await session.execute(select(func.count(Passenger.id)))
        return int(result.scalar() or 0)
