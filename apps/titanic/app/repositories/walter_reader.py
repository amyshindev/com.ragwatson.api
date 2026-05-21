from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

# Resolves to backend/apps/titanic/app
_DATA_DIR = Path(__file__).resolve().parent.parent
_CSV_PATH = _DATA_DIR / "Titanic-Dataset.csv"


class WalterReader:
    def __init__(self, session: AsyncSession | None = None) -> None:
        self.session = session

    def get_data(self) -> pd.DataFrame:
        """Synchronously reads first passenger row from CSV."""
        df = pd.read_csv(_CSV_PATH)
        return df.iloc[[0]].astype(object).where(df.iloc[[0]].notna(), None)

    async def get_data_db(self) -> pd.DataFrame:
        """Asynchronously reads first passenger row from DB if session exists; else CSV."""
        if self.session is None:
            return self.get_data()

        from titanic.app.models.passenger import Passenger

        result = await self.session.execute(
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

    def get_count(self) -> int:
        """Synchronously gets passenger count from CSV."""
        df = pd.read_csv(_CSV_PATH)
        return int(df.shape[0])

    async def get_count_db(self) -> int:
        """Asynchronously gets passenger count from DB if session exists; else CSV."""
        if self.session is None:
            return self.get_count()

        from titanic.app.models.passenger import Passenger

        result = await self.session.execute(select(func.count(Passenger.id)))
        return int(result.scalar() or 0)

    def get_dataframe(self) -> pd.DataFrame:
        """Synchronously gets full DataFrame from CSV."""
        return pd.read_csv(_CSV_PATH)

    async def get_dataframe_db(self) -> pd.DataFrame:
        """Asynchronously gets full DataFrame from DB if session exists; else CSV."""
        if self.session is None:
            return self.get_dataframe()

        from titanic.app.models.passenger import Passenger

        result = await self.session.execute(select(Passenger))
        passengers = result.scalars().all()
        if not passengers:
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
        return pd.DataFrame(data)
