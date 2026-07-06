from pydantic import BaseModel, Field


class HudsonHousekeeperSchema(BaseModel):
    id: int = Field(4, description="Character ID")
    name: str = Field("허드슨", description="Character name")
    # 221B 하우스키퍼·현장 접수

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "미스 허드슨 (Mrs. Hudson)",
            }
        }
    }
