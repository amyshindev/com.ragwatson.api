from typing import Any

from pydantic import BaseModel, Field


class FordDirectorSchema(BaseModel):
    id: int = Field(1, description="Character ID")
    name: str = Field("Robert Ford (Director)", description="Character name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Robert Ford (Director)",
            }
        }
    }


class FordDirectorTriggerSchema(BaseModel):
    workflow: str = Field("default", description="n8n workflow identifier")
    payload: dict[str, Any] = Field(default_factory=dict, description="Event body for n8n")

    model_config = {
        "json_schema_extra": {
            "example": {
                "workflow": "star-craft-route",
                "payload": {"source": "titanic", "event": "passenger.created"},
            }
        }
    }
