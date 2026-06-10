from pydantic import BaseModel, Field

class RuthValidationSchema(BaseModel):
    
    id: int = Field(9, description="Passenger ID")
    name: str = Field("루스 드윗 부케이터", description="Passenger's name")
    # 검증 담당 승객
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 11,
                "name": "Ruth DeWitt Bukater",
            }
        }
    }
