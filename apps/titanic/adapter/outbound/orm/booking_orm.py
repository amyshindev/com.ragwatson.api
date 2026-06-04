from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.matrix.oracle_database import Base
from titanic.app.dtos.james_dto import BookingCommand

if TYPE_CHECKING:
    from titanic.adapter.outbound.orm.person_orm import PersonOrm


class BookingOrm(Base):
    __tablename__ = "titanic_bookings"

    passenger_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("titanic_persons.passenger_id", ondelete="CASCADE"),
        primary_key=True,
    )
    pclass: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    ticket: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    fare: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    cabin: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    embarked: Mapped[str] = mapped_column(String(8), nullable=False, default="")

    person: Mapped[PersonOrm] = relationship(back_populates="bookings")

    @classmethod
    def from_command(cls, command: BookingCommand, *, passenger_id: int) -> BookingOrm:
        return cls(
            passenger_id=passenger_id,
            pclass=command.pclass,
            ticket=command.ticket,
            fare=command.fare,
            cabin=command.cabin,
            embarked=command.embarked,
        )

    def apply_command(self, command: BookingCommand) -> None:
        self.pclass = command.pclass
        self.ticket = command.ticket
        self.fare = command.fare
        self.cabin = command.cabin
        self.embarked = command.embarked
