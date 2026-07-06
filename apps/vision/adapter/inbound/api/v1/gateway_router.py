from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from vision.adapter.inbound.api.schemas.gateway_schema import (
    VisionCharacterListSchema,
    VisionCharacterSchema,
    VisionUploadResponseSchema,
)
from vision.app.constants.vision_characters import VISION_CHARACTERS
from vision.app.use_cases.vision_gateway_interactor import VisionGatewayInteractor
from vision.dependencies.gateway_provider import get_vision_gateway_interactor

log = logging.getLogger(__name__)

gateway_router = APIRouter(prefix="/vision", tags=["vision"])


@gateway_router.get("/characters", response_model=VisionCharacterListSchema)
async def list_vision_characters(
    gateway: VisionGatewayInteractor = Depends(get_vision_gateway_interactor),
) -> VisionCharacterListSchema:
    return await gateway.list_characters()


@gateway_router.post("/upload", response_model=VisionUploadResponseSchema)
async def upload_vision_image(
    file: UploadFile = File(...),
    gateway: VisionGatewayInteractor = Depends(get_vision_gateway_interactor),
) -> VisionUploadResponseSchema:
    log.info("[GatewayRouter] upload filename=%s", file.filename)
    try:
        data = await file.read()
        return await gateway.upload_image(
            filename=file.filename or "upload.bin",
            content_type=file.content_type or "",
            data=data,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
