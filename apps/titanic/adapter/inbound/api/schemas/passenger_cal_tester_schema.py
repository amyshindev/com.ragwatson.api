from pydantic import BaseModel, Field


class CalTesterSchema(BaseModel):
    id: int = Field(4, description="Passenger ID")
    name: str = Field("캘러든 호클리", description="Passenger's name")
    # 1등석 승객 , 탑승 데이터 유효성 검증 테스터 역할

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 6,
                "name": "Caledon Hockley",
            }
        }
    }
