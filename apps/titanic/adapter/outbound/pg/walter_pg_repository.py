import logging

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)


class WalterPgRepository:
    """Walter output port에서 전달된 조회 요청을 Neon DB(passengers)에서 수행."""

    async def get_dataframe_db(self, session: AsyncSession) -> pd.DataFrame:
        from titanic.app.use_cases.passenger import Passenger

        log.info("[WalterPgRepository] DB 조회 시작 — passengers")
        result = await session.execute(
            select(Passenger).order_by(Passenger.passenger_id.asc())
        )
        passengers = result.scalars().all()
        if not passengers:
            log.info("[WalterPgRepository] DB 조회 결과 없음")
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
        log.info("[WalterPgRepository] DB 조회 완료 — rows=%s", len(passengers))
        return pd.DataFrame(data)

