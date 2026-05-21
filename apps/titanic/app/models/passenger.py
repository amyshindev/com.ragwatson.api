from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Passenger(Base):
    __tablename__ = "passengers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[int] = mapped_column(unique=True, index=True, nullable=False)
    survived: Mapped[int] = mapped_column(nullable=False)
    pclass: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sex: Mapped[str] = mapped_column(String(10), nullable=False)
    age: Mapped[float | None] = mapped_column(nullable=True)
    sibsp: Mapped[int] = mapped_column(nullable=False)
    parch: Mapped[int] = mapped_column(nullable=False)
    ticket: Mapped[str] = mapped_column(String(50), nullable=False)
    fare: Mapped[float] = mapped_column(nullable=False)
    cabin: Mapped[str | None] = mapped_column(String(50), nullable=True)
    boat: Mapped[str | None] = mapped_column(String(50), nullable=True)
    embarked: Mapped[str | None] = mapped_column(String(10), nullable=True)
