from pydantic import BaseModel, Field

class HartleyViolinSchema(BaseModel):
    
    id: int = Field(1, description="Violinist ID")
    name: str = Field("월리스 하틀리", description="Violinist's name")
    # 타이타닉 밴드 리더 , 침몰 시 바이올린을 연주하며 승객들을 위로함
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": "Wallace Hartley",
            }
        }
    }
