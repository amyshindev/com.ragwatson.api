from pydantic import BaseModel, Field


class HendricksCeoSchema(BaseModel):
    id: int = Field(1, description="Character ID")
    name: str = Field("Richard Hendricks (CEO)", description="Character name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Richard Hendricks (CEO)",
            }
        }
    }
