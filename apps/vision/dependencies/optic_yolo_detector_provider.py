from vision.app.ports.input.optic_yolo_detector_use_case import YoloDetectorUseCase
from vision.app.use_cases.optic_yolo_detector_interactor import YoloDetectorInteractor

_singleton: YoloDetectorInteractor | None = None


def get_optic_yolo_detector_use_case() -> YoloDetectorUseCase:
    global _singleton
    if _singleton is None:
        _singleton = YoloDetectorInteractor()
    return _singleton
