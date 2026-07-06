from pydantic import BaseModel, Field


class LestradeOfficialSchema(BaseModel):
    id: int = Field(3, description="Character ID")
    name: str = Field("레스트레이드", description="Character name")
    # 스코트랜드야드 공식 수사

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": "인스펙터 레스트레이드 (Inspector Lestrade)",
            }
        }
    }
