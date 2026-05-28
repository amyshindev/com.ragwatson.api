from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from titanic.domain.entities.titanic import TitanicPassenger


class TitanicPassengerCreateRequest(BaseModel):
    """타이타닉 승객 생성 요청 (모든 필드 str, sex → gender)."""

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

    def to_entity(self) -> TitanicPassenger:
        from titanic.domain.entities.titanic import TitanicPassenger

        return TitanicPassenger(
            passenger_id=self.passenger_id,
            survived=self.survived,
            pclass=self.pclass,
            name=self.name,
            gender=self.gender,
            age=self.age,
            sibsp=self.sibsp,
            parch=self.parch,
            ticket=self.ticket,
            fare=self.fare,
            cabin=self.cabin,
            embarked=self.embarked,
        )
