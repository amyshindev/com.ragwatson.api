from pydantic import BaseModel, ConfigDict, Field

from titanic.domain.entities.titanic import TitanicPassenger


class TitanicPassengerCreateResponse(BaseModel):
    """타이타닉 승객 생성 응답 (모든 필드 str, sex → gender)."""

    id: str = Field(..., description="DB primary key")
    passenger_id: str = Field(..., alias="PassengerId", description="승객 ID")
    survived: str = Field(..., alias="Survived", description="생존 여부")
    pclass: str = Field(..., alias="Pclass", description="티켓 클래스")
    name: str = Field(..., alias="Name", description="이름")
    gender: str = Field(..., alias="Gender", description="성별")
    age: str = Field(default="", alias="Age", description="나이")
    sibsp: str = Field(..., alias="SibSp", description="형제/배우자 수")
    parch: str = Field(..., alias="Parch", description="부모/자녀 수")
    ticket: str = Field(..., alias="Ticket", description="티켓 번호")
    fare: str = Field(..., alias="Fare", description="요금")
    cabin: str = Field(default="", alias="Cabin", description="객실")
    embarked: str = Field(default="", alias="Embarked", description="승선 항구")

    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    def from_entity(cls, db_id: int, passenger: TitanicPassenger) -> "TitanicPassengerCreateResponse":
        return cls(
            id=str(db_id),
            passenger_id=passenger.passenger_id,
            survived=passenger.survived,
            pclass=passenger.pclass,
            name=passenger.name,
            gender=passenger.gender,
            age=passenger.age,
            sibsp=passenger.sibsp,
            parch=passenger.parch,
            ticket=passenger.ticket,
            fare=passenger.fare,
            cabin=passenger.cabin,
            embarked=passenger.embarked,
        )
