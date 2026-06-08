from pydantic import BaseModel, Field


class PassengerMollyScalerSchema(BaseModel):

    id: int = Field(7, description="Passenger ID")
    name: str = Field("몰리 브라운", description="Passenger's name")
    # 생존자, 피처 스케일링 담당 승객

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 9,
                "name": "Molly Brown",
            }
        }
    }
