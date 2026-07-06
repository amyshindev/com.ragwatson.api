from pydantic import BaseModel, Field


class SherlockHolmesSchema(BaseModel):
    id: int = Field(1, description="Character ID")
    name: str = Field("셜록 홈즈", description="Character name")
    # 베이커가 221B, 추론·단서 분석

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "셜록 홈즈 (Sherlock Holmes)",
            }
        }
    }
