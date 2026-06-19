from pydantic import BaseModel, Field


class BighettiHrSchema(BaseModel):

    id: int = Field(5, description="Character ID")
    name: str = Field('Bighetti (HR)', description="Character name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": 'Bighetti (HR)',
            }
        }
    }
