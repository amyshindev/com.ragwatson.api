from pydantic import BaseModel, Field


class ResnetClassifierSchema(BaseModel):
    id: int = Field(1, description="Character ID")
    name: str = Field("레즈넷 (ResNet)", description="Character name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "레즈넷 (ResNet)",
            }
        }
    }
