from pydantic import BaseModel, Field


class DunnCooSchema(BaseModel):

    id: int = Field(4, description="Character ID")
    name: str = Field('Dunn (COO)', description="Character name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": 'Dunn (COO)',
            }
        }
    }
