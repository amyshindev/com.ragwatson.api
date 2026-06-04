from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.matrix.oracle_database import Base
from titanic.app.dtos.james_dto import PersonCommand

if TYPE_CHECKING:
    from titanic.adapter.outbound.orm.booking_orm import BookingOrm


class PersonOrm(Base):
    __tablename__ = "titanic_persons"

    passenger_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    gender: Mapped[str] = mapped_column(String(16), nullable=False, default="")
    age: Mapped[str] = mapped_column(String(16), nullable=False, default="")
    sib_sp: Mapped[str] = mapped_column(String(16), nullable=False, default="")
    parch: Mapped[str] = mapped_column(String(16), nullable=False, default="")
    survived: Mapped[str] = mapped_column(String(8), nullable=False, default="")

    bookings: Mapped[list[BookingOrm]] = relationship(
        back_populates="person",
        cascade="all, delete-orphan",
    )

    @classmethod
    def from_command(cls, command: PersonCommand) -> PersonOrm:
        return cls(
            passenger_id=command.passenger_id,
            name=command.name,
            gender=command.gender,
            age=command.age,
            sib_sp=command.sib_sp,
            parch=command.parch,
            survived=command.survived,
        )

    def apply_command(self, command: PersonCommand) -> None:
        self.name = command.name
        self.gender = command.gender
        self.age = command.age
        self.sib_sp = command.sib_sp
        self.parch = command.parch
        self.survived = command.survived
