from fastapi import APIRouter, Depends

from vision.adapter.inbound.api.schemas.optic_clip_embedder_schema import ClipEmbedderSchema
from vision.app.dtos.optic_clip_embedder_dto import ClipEmbedderResponse
from vision.app.ports.input.optic_clip_embedder_use_case import ClipEmbedderUseCase
from vision.dependencies.optic_clip_embedder_provider import get_optic_clip_embedder_use_case

optic_clip_embedder_router = APIRouter(prefix="/vision/clip", tags=["vision", "clip"])


@optic_clip_embedder_router.get("/myself")
async def introduce_myself(
    character: ClipEmbedderUseCase = Depends(get_optic_clip_embedder_use_case),
) -> ClipEmbedderResponse:
    return await character.introduce_myself(
        ClipEmbedderSchema(id=1, name="클립 (CLIP)")
    )
