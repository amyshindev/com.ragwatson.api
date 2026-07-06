from pydantic import BaseModel, Field


class WatsonChroniclerSchema(BaseModel):
    id: int = Field(2, description="Character ID")
    name: str = Field("왓슨", description="Character name")
    # 동반자·사건 기록자

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": "존 H. 왓슨 (Dr. John Watson)",
            }
        }
    }
