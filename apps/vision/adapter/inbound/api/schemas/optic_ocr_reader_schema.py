from pydantic import BaseModel, Field


class OcrReaderSchema(BaseModel):
    id: int = Field(1, description="Character ID")
    name: str = Field("OCR 리더", description="Character name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "OCR 리더",
            }
        }
    }
