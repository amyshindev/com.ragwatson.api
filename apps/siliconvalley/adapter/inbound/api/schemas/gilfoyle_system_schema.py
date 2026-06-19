from pydantic import BaseModel, Field


class GilfoyleSystemSchema(BaseModel):

    id: int = Field(2, description="Character ID")
    name: str = Field('Bertram Gilfoyle (System)', description="Character name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": 'Bertram Gilfoyle (System)',
            }
        }
    }
