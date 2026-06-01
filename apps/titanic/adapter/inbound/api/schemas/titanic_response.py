from pydantic import BaseModel, ConfigDict

from titanic.domain.entities.titanic import TitanicPassenger


class TitanicPassengerCreateResponse(BaseModel):
    """타이타닉 승객 조회/생성 응답."""

    passenger_id: int
    survived: int
    pclass: int
    name: str
    sex: str
    age: float | None
    sibsp: int
    parch: int
    ticket: str
    fare: float
    cabin: str | None
    boat: str | None
    embarked: str | None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, passenger: TitanicPassenger) -> "TitanicPassengerCreateResponse":
        age: float | None = None
        if passenger.age:
            age = float(passenger.age)

        return cls(
            passenger_id=int(passenger.passenger_id),
            survived=int(passenger.survived),
            pclass=int(passenger.pclass),
            name=passenger.name,
            sex=passenger.gender,
            age=age,
            sibsp=int(passenger.sibsp),
            parch=int(passenger.parch),
            ticket=passenger.ticket,
            fare=float(passenger.fare),
            cabin=passenger.cabin or None,
            boat=None,
            embarked=passenger.embarked or None,
        )
