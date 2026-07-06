from pydantic import BaseModel, Field


class SamSegmenterSchema(BaseModel):
    id: int = Field(1, description="Character ID")
    name: str = Field("샘 (SAM)", description="Character name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "샘 (SAM)",
            }
        }
    }
