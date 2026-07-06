from __future__ import annotations

from vision.adapter.inbound.api.schemas.optic_clip_embedder_schema import ClipEmbedderSchema
from vision.app.dtos.optic_clip_embedder_dto import ClipEmbedderQuery, ClipEmbedderResponse
from vision.app.ports.input.optic_clip_embedder_use_case import ClipEmbedderUseCase
from vision.app.ports.output.optic_clip_embedder_port import ClipEmbedderPort


class ClipEmbedderInteractor(ClipEmbedderUseCase):
    def __init__(self, repository: ClipEmbedderPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: ClipEmbedderSchema) -> ClipEmbedderResponse:
        return await self._repository.introduce_myself(
            ClipEmbedderQuery(id=schema.id, name=schema.name)
        )
