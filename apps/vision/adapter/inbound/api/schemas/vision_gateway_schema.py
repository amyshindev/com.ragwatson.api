from pydantic import BaseModel, Field


class VisionCharacterSchema(BaseModel):
    id: str
    route: str
    name: str
    role: str
    myself_path: str


class VisionCharacterListSchema(BaseModel):
    items: list[VisionCharacterSchema]


class VisionUploadResponseSchema(BaseModel):
    ok: bool = True
    file_id: str
    filename: str
    content_type: str
    size_bytes: int
    storage: str = "memory"
    s3_bucket: str | None = None
    s3_key: str | None = None
    s3_url: str | None = None
    message: str = Field(default="이미지 업로드가 완료되었습니다.")
