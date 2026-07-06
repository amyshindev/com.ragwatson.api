from fastapi import APIRouter, Depends

from vision.adapter.inbound.api.schemas.optic_ocr_reader_schema import OcrReaderSchema
from vision.app.dtos.optic_ocr_reader_dto import OcrReaderResponse
from vision.app.ports.input.optic_ocr_reader_use_case import OcrReaderUseCase
from vision.dependencies.optic_ocr_reader_provider import get_optic_ocr_reader_use_case

optic_ocr_reader_router = APIRouter(prefix="/vision/ocr", tags=["vision", "ocr"])


@optic_ocr_reader_router.get("/myself")
async def introduce_myself(
    character: OcrReaderUseCase = Depends(get_optic_ocr_reader_use_case),
) -> OcrReaderResponse:
    return await character.introduce_myself(
        OcrReaderSchema(id=1, name="OCR 리더")
    )
