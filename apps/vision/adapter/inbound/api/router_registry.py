from fastapi import APIRouter

from vision.adapter.inbound.api.v1.gateway_router import gateway_router
from vision.adapter.inbound.api.v1.optic_yolo_detector_router import optic_yolo_detector_router

vision_router = APIRouter()
vision_router.include_router(gateway_router)
vision_router.include_router(optic_yolo_detector_router)

__all__ = ["vision_router"]
