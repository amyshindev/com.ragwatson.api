from pydantic import BaseModel, Field


class PassengerIsidorCoupleSchema(BaseModel):

    id: int = Field(5, description="Passenger ID")
    name: str = Field("이시도르 스트라우스", description="Passenger's name")
    # 1등석 승객, 부인과 함께 탑승한 부부

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 7,
                "name": "Isidor Straus",
            }
        }
    }
