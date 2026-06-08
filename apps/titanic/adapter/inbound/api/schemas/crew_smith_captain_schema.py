from pydantic import BaseModel, Field


class CrewSmithCaptainSchema(BaseModel):

    id: int = Field(3, description="Captain ID")
    name: str = Field("에드워드 스미스", description="Captain's name")
    # 타이타닉호 선장, 최종 항해를 지휘함

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Edward Smith",
            }
        }
    }
