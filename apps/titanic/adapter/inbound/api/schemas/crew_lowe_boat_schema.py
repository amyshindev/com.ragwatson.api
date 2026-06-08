from pydantic import BaseModel, Field


class CrewLoweBoatSchema(BaseModel):

    id: int = Field(2, description="Officer ID")
    name: str = Field("해롤드 로우", description="Officer's name")
    # 5등 항해사, 구명보트 배정과 구조 작전을 담당함

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "Harold Lowe",
            }
        }
    }
