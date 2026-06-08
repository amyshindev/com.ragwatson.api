from pydantic import BaseModel, Field


class CrewWalterRoasterSchema(BaseModel):

    id: int = Field(1, description="Crew ID")
    name: str = Field("월터", description="Crew member's name")
    # 타이타닉 일등 항해사, 승객 명단 관리 담당

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Hugh Walter McElroy",
            }
        }
    }
