from pydantic import BaseModel, Field


class MoriartyRivalSchema(BaseModel):
    id: int = Field(6, description="Character ID")
    name: str = Field("모리어티", description="Character name")
    # 적대 검증·리스크 시나리오

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 6,
                "name": "프로페서 모리어티 (Professor Moriarty)",
            }
        }
    }
