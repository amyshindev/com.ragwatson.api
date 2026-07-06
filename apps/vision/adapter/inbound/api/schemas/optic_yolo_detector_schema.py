from pydantic import BaseModel, Field


class YoloDetectorSchema(BaseModel):
    id: int = Field(1, description="Character ID")
    name: str = Field("요로 (YOLO)", description="Character name")
