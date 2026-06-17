from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.grid_neo_theone_base import Base
from titanic.app.dtos.crew_james_director_dto import BookingCommand

if TYPE_CHECKING:
    from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PassengerJackTrainerOrm


class PassengerRoseModelOrm(Base):
    __tablename__ = "bookings"

    passenger_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("passengers.passenger_id", ondelete="CASCADE"),
        primary_key=True,
    )
    pclass: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    ticket: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    fare: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    cabin: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    embarked: Mapped[str] = mapped_column(String(8), nullable=False, default="")

    passengers: Mapped[PassengerJackTrainerOrm] = relationship(back_populates="bookings")

    @classmethod
    def from_command(cls, command: BookingCommand, *, passenger_id: str) -> PassengerRoseModelOrm:
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
