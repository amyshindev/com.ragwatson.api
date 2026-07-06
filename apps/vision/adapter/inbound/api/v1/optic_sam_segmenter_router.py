from fastapi import APIRouter, Depends

from vision.adapter.inbound.api.schemas.optic_sam_segmenter_schema import SamSegmenterSchema
from vision.app.dtos.optic_sam_segmenter_dto import SamSegmenterResponse
from vision.app.ports.input.optic_sam_segmenter_use_case import SamSegmenterUseCase
from vision.dependencies.optic_sam_segmenter_provider import get_optic_sam_segmenter_use_case

optic_sam_segmenter_router = APIRouter(prefix="/vision/sam", tags=["vision", "sam"])


@optic_sam_segmenter_router.get("/myself")
async def introduce_myself(
    character: SamSegmenterUseCase = Depends(get_optic_sam_segmenter_use_case),
) -> SamSegmenterResponse:
    return await character.introduce_myself(
        SamSegmenterSchema(id=1, name="샘 (SAM)")
    )
