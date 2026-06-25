from pydantic import BaseModel, Field


class RoseModelSchema(BaseModel):
    id: int = Field(8, description="Passenger ID")
    name: str = Field("로즈 드윗 부케이터", description="Passenger's name")
    # 1등석 승객 , 의사결정나무 생존 모델 소유

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 10,
                "name": "Rose DeWitt Bukater",
            }
        }
    }
