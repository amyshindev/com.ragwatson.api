import logging

from sqlalchemy import select

import database
from core.config import is_database_configured
from titanic.app.models.passenger import Passenger
from titanic.app.repositories.walter_reader import WalterReader

log = logging.getLogger(__name__)


async def init_titanic_tables() -> None:
    if not is_database_configured():
        log.info("Titanic DB initialization skipped (DATABASE_URL not set)")
        return

    from orm_registry import import_all_models

    import_all_models()

    await database.init_db()
    database._ensure_engine()
    assert database.engine is not None

    async with database.AsyncSessionLocal() as session:
        async with session.begin():
            # Check if Passenger table already has data
            result = await session.execute(select(Passenger).limit(1))
            passenger = result.scalar_one_or_none()
            if passenger is None:
                log.info("Titanic passengers table is empty. Seeding from CSV...")
                reader = WalterReader()
                df = reader.get_dataframe()

                count = 0
                for _, row in df.iterrows():
                    # Handle NaNs in Pandas safely
                    def clean_val(v):
                        import pandas as pd

                        if pd.isna(v):
                            return None
                        return v

                    # Handle boat if column does not exist in CSV
                    boat_val = clean_val(row.get("Boat")) if "Boat" in row else None

                    p = Passenger(
                        passenger_id=int(row["PassengerId"]),
                        survived=int(row["Survived"]),
                        pclass=int(row["Pclass"]),
                        name=str(row["Name"]),
                        sex=str(row["Sex"]),
                        age=clean_val(row.get("Age")),
                        sibsp=int(row["SibSp"]),
                        parch=int(row["Parch"]),
                        ticket=str(row["Ticket"]),
                        fare=float(row["Fare"]),
                        cabin=clean_val(row.get("Cabin")),
                        boat=boat_val,
                        embarked=clean_val(row.get("Embarked")),
                    )
                    session.add(p)
                    count += 1
                log.info("Seeded %d passengers into the database.", count)
            else:
                log.info("Titanic passengers table already contains data. Seeding skipped.")
