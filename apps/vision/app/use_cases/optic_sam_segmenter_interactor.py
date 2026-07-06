from __future__ import annotations

from vision.adapter.inbound.api.schemas.optic_sam_segmenter_schema import SamSegmenterSchema
from vision.app.dtos.optic_sam_segmenter_dto import SamSegmenterQuery, SamSegmenterResponse
from vision.app.ports.input.optic_sam_segmenter_use_case import SamSegmenterUseCase
from vision.app.ports.output.optic_sam_segmenter_port import SamSegmenterPort


class SamSegmenterInteractor(SamSegmenterUseCase):
    def __init__(self, repository: SamSegmenterPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: SamSegmenterSchema) -> SamSegmenterResponse:
        return await self._repository.introduce_myself(
            SamSegmenterQuery(id=schema.id, name=schema.name)
        )
