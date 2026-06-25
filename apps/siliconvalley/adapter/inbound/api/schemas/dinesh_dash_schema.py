from pydantic import BaseModel, Field


class DineshDashSchema(BaseModel):
    id: int = Field(3, description="Character ID")
    name: str = Field("Dinesh Chugtai (Dash)", description="Character name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": "Dinesh Chugtai (Dash)",
            }
        }
    }
