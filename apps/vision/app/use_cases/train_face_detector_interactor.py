"""하위 호환 — TrainYoloInteractor를 Face 이름으로 노출."""

from vision.app.dtos.yolo_train_dto import YoloTrainHyperparams as FaceTrainHyperparams
from vision.app.dtos.yolo_train_dto import YoloTrainResult as FaceTrainResult
from vision.app.use_cases.train_yolo_interactor import TrainYoloInteractor

TrainFaceDetectorInteractor = TrainYoloInteractor

__all__ = [
    "FaceTrainHyperparams",
    "FaceTrainResult",
    "TrainFaceDetectorInteractor",
    "TrainYoloInteractor",
]
