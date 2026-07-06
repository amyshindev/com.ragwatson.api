from fastapi import APIRouter, Depends

from vision.adapter.inbound.api.schemas.optic_resnet_classifier_schema import ResnetClassifierSchema
from vision.app.dtos.optic_resnet_classifier_dto import ResnetClassifierResponse
from vision.app.ports.input.optic_resnet_classifier_use_case import ResnetClassifierUseCase
from vision.dependencies.optic_resnet_classifier_provider import get_optic_resnet_classifier_use_case

optic_resnet_classifier_router = APIRouter(prefix="/vision/resnet", tags=["vision", "resnet"])


@optic_resnet_classifier_router.get("/myself")
async def introduce_myself(
    character: ResnetClassifierUseCase = Depends(get_optic_resnet_classifier_use_case),
) -> ResnetClassifierResponse:
    return await character.introduce_myself(
        ResnetClassifierSchema(id=1, name="레즈넷 (ResNet)")
    )
