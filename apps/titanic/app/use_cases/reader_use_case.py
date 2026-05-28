import logging

import pandas as pd
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)


class WalterReader:
    def __init__(self, session: AsyncSession | None = None) -> None:
        self.session = session

    def _require_session(self) -> AsyncSession:
        if self.session is None:
            raise RuntimeError("Titanic data requires a database session.")
        return self.session

    async def get_data_db(self) -> pd.DataFrame:
        """Asynchronously reads first passenger row from DB."""
        session = self._require_session()

        from titanic.app.use_cases.passenger import Passenger

        result = await session.execute(
            select(Passenger).order_by(Passenger.passenger_id).limit(1)
        )
        passenger = result.scalar_one_or_none()
        if passenger is None:
            return pd.DataFrame()

        data = {
            "PassengerId": [passenger.passenger_id],
            "Survived": [passenger.survived],
            "Pclass": [passenger.pclass],
            "Name": [passenger.name],
            "Sex": [passenger.sex],
            "Age": [passenger.age],
            "SibSp": [passenger.sibsp],
            "Parch": [passenger.parch],
            "Ticket": [passenger.ticket],
            "Fare": [passenger.fare],
            "Cabin": [passenger.cabin],
            "Boat": [passenger.boat],
            "Embarked": [passenger.embarked],
        }
        return pd.DataFrame(data)

    async def get_count_db(self) -> int:
        """Asynchronously gets passenger count from DB."""
        session = self._require_session()

        from titanic.app.use_cases.passenger import Passenger

        result = await session.execute(select(func.count(Passenger.id)))
        return int(result.scalar() or 0)

    async def get_dataframe_db(self) -> pd.DataFrame:
        """Asynchronously gets full DataFrame from DB."""
        log.info("[WalterReaderUseCase] DB 조회 시작 — get_dataframe_db")
        session = self._require_session()

        from titanic.app.use_cases.passenger import Passenger

        result = await session.execute(
            select(Passenger).order_by(Passenger.passenger_id.asc())
        )
        passengers = result.scalars().all()
        if not passengers:
            log.info("[WalterReaderUseCase] DB 조회 결과 없음")
            return pd.DataFrame()

        data = {
            "PassengerId": [p.passenger_id for p in passengers],
            "Survived": [p.survived for p in passengers],
            "Pclass": [p.pclass for p in passengers],
            "Name": [p.name for p in passengers],
            "Sex": [p.sex for p in passengers],
            "Age": [p.age for p in passengers],
            "SibSp": [p.sibsp for p in passengers],
            "Parch": [p.parch for p in passengers],
            "Ticket": [p.ticket for p in passengers],
            "Fare": [p.fare for p in passengers],
            "Cabin": [p.cabin for p in passengers],
            "Boat": [p.boat for p in passengers],
            "Embarked": [p.embarked for p in passengers],
        }
        log.info("[WalterReaderUseCase] DB 조회 완료 — rows=%s", len(passengers))
        return pd.DataFrame(data)
