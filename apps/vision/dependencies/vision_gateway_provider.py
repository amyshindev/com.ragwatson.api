from core.config import is_vision_s3_configured
from vision.adapter.outbound.memory.vision_upload_memory_repository import (
    VisionUploadMemoryRepository,
)
from vision.adapter.outbound.s3.vision_upload_s3_repository import VisionUploadS3Repository
from vision.app.ports.output.vision_upload_port import VisionUploadPort
from vision.app.use_cases.vision_gateway_interactor import VisionGatewayInteractor

_upload_singleton: VisionUploadPort | None = None
_gateway_singleton: VisionGatewayInteractor | None = None


def get_vision_upload_repository() -> VisionUploadPort:
    global _upload_singleton
    if _upload_singleton is None:
        if is_vision_s3_configured():
            _upload_singleton = VisionUploadS3Repository()
        else:
            _upload_singleton = VisionUploadMemoryRepository()
    return _upload_singleton


def get_vision_gateway_interactor() -> VisionGatewayInteractor:
    global _gateway_singleton
    if _gateway_singleton is None:
        _gateway_singleton = VisionGatewayInteractor(
            upload_repository=get_vision_upload_repository(),
        )
    return _gateway_singleton
