from pydantic import BaseModel, Field


class PassengerJackTrainerSchema(BaseModel):

    id: int = Field(6, description="Passenger ID")
    name: str = Field("잭 도슨", description="Passenger's name")
    # 3등석 승객, 생존 예측 모델 학습 담당

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 8,
                "name": "Jack Dawson",
            }
        }
    }
