import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from vision.adapter.inbound.api.schemas.vision_gateway_schema import (
    VisionCharacterListSchema,
    VisionUploadResponseSchema,
)
from vision.adapter.inbound.api.v1.vision_s3_upload import (
    save_vision_image_to_s3,
    vision_s3_enabled,
)
from vision.app.dtos.vision_gateway_dto import VisionUploadCommand
from vision.app.use_cases.vision_gateway_interactor import VisionGatewayInteractor
from vision.dependencies.vision_gateway_provider import get_vision_gateway_interactor

log = logging.getLogger(__name__)

vision_gateway_router = APIRouter(prefix="/vision", tags=["vision"])

_ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/bmp",
}
_MAX_BYTES = 10 * 1024 * 1024


def _accept_image_upload(file: UploadFile) -> bool:
    content_type = (file.content_type or "").split(";")[0].strip().lower()
    if content_type.startswith("image/"):
        return True
    filename = (file.filename or "").lower()
    return filename.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"))


def _normalize_content_type(content_type: str) -> str:
    return (content_type or "").split(";")[0].strip().lower()


@vision_gateway_router.get("/characters", response_model=VisionCharacterListSchema)
async def list_vision_characters(
    gateway: VisionGatewayInteractor = Depends(get_vision_gateway_interactor),
) -> VisionCharacterListSchema:
    return await gateway.list_characters()


@vision_gateway_router.post("/upload", response_model=VisionUploadResponseSchema)
async def upload_vision_image(
    file: UploadFile = File(...),
    gateway: VisionGatewayInteractor = Depends(get_vision_gateway_interactor),
) -> VisionUploadResponseSchema:
    """프론트엔드 이미지 업로드 → AWS S3 버킷 저장 (VISION_S3_BUCKET / AWS_S3_BUCKET)."""
    log.info(
        "[VisionGatewayRouter] upload filename=%s s3_enabled=%s",
        file.filename,
        vision_s3_enabled(),
    )
    if not _accept_image_upload(file):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드할 수 있습니다.")

    try:
        data = await file.read()
        filename = file.filename or "upload.bin"
        content_type = _normalize_content_type(file.content_type or "")

        if len(data) == 0:
            raise ValueError("빈 파일입니다.")
        if len(data) > _MAX_BYTES:
            raise ValueError("이미지 크기는 10MB 이하여야 합니다.")
        if content_type not in _ALLOWED_IMAGE_TYPES and not content_type.startswith("image/"):
            raise ValueError("이미지 파일만 업로드할 수 있습니다.")

        if vision_s3_enabled():
            saved = await save_vision_image_to_s3(
                VisionUploadCommand(
                    filename=filename,
                    content_type=content_type or "application/octet-stream",
                    size_bytes=len(data),
                    data=data,
                ),
            )
            return VisionUploadResponseSchema(
                file_id=saved.file_id,
                filename=saved.filename,
                content_type=saved.content_type,
                size_bytes=saved.size_bytes,
                storage=saved.storage,
                s3_bucket=saved.s3_bucket,
                s3_key=saved.s3_key,
                s3_url=saved.s3_url,
                message="이미지가 S3에 저장되었습니다.",
            )

        return await gateway.upload_image(
            filename=filename,
            content_type=content_type,
            data=data,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
