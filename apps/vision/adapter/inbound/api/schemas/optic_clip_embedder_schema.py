from pydantic import BaseModel, Field


class ClipEmbedderSchema(BaseModel):
    id: int = Field(1, description="Character ID")
    name: str = Field("클립 (CLIP)", description="Character name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "클립 (CLIP)",
            }
        }
    }
