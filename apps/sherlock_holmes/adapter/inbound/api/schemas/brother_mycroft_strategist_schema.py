from pydantic import BaseModel, Field


class MycroftStrategistSchema(BaseModel):
    id: int = Field(5, description="Character ID")
    name: str = Field("마이크로프트", description="Character name")
    # 전략·정보 조율

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "마이크로프트 홈즈 (Mycroft Holmes)",
            }
        }
    }
