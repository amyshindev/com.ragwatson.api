from pydantic import BaseModel, Field


class PassengerSchema(BaseModel):
    passenger_id: int = Field(..., alias="PassengerId", description="승객 ID")
    survived: int = Field(..., alias="Survived", description="생존 여부 (0 = 사망, 1 = 생존)")
    pclass: int = Field(..., alias="Pclass", description="티켓 클래스 (1 = 1등석, 2 = 2등석, 3 = 3등석)")
    name: str = Field(..., alias="Name", description="이름")
    sex: str = Field(..., alias="Sex", description="성별")
    age: float | None = Field(default=None, alias="Age", description="나이")
    sibsp: int = Field(..., alias="SibSp", description="함께 탑승한 자녀 / 배우자의 수")
    parch: int = Field(..., alias="Parch", description="함께 탑승한 부모님 / 아이들의 수")
    ticket: str = Field(..., alias="Ticket", description="티켓 번호")
    fare: float = Field(..., alias="Fare", description="탑승 요금")
    cabin: str | None = Field(default=None, alias="Cabin", description="수하물 번호")
    boat: str | None = Field(default=None, alias="Boat", description="탈출한 보트 번호")
    embarked: str | None = Field(default=None, alias="Embarked", description="선착장 (C, Q, S)")

    class Config:
        populate_by_name = True
        from_attributes = True


class PassengerResponse(BaseModel):
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

    class Config:
        from_attributes = True
