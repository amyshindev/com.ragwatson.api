from __future__ import annotations

from vision.adapter.inbound.api.schemas.optic_resnet_classifier_schema import ResnetClassifierSchema
from vision.app.dtos.optic_resnet_classifier_dto import ResnetClassifierQuery, ResnetClassifierResponse
from vision.app.ports.input.optic_resnet_classifier_use_case import ResnetClassifierUseCase
from vision.app.ports.output.optic_resnet_classifier_port import ResnetClassifierPort


class ResnetClassifierInteractor(ResnetClassifierUseCase):
    def __init__(self, repository: ResnetClassifierPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: ResnetClassifierSchema) -> ResnetClassifierResponse:
        return await self._repository.introduce_myself(
            ResnetClassifierQuery(id=schema.id, name=schema.name)
        )
