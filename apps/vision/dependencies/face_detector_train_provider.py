from vision.adapter.outbound.detection.local_yolo_base_weights_adapter import (
    LocalYoloBaseWeightsAdapter,
)
from vision.adapter.outbound.detection.local_yolo_face_dataset_adapter import (
    LocalYoloFaceDatasetAdapter,
)
from vision.adapter.outbound.detection.local_face_model_checkpoint_adapter import (
    LocalFaceModelCheckpointAdapter,
)
from vision.adapter.outbound.detection.local_yolo_train_device_adapter import (
    LocalYoloTrainDeviceAdapter,
)
from vision.adapter.outbound.detection.local_yolo_train_run_adapter import (
    LocalYoloTrainRunAdapter,
)
from vision.app.ports.input.train_yolo_use_case import TrainYoloUseCase
from vision.app.ports.output.face_dataset_port import FaceDatasetPort
from vision.app.ports.output.face_model_checkpoint_port import FaceModelCheckpointPort
from vision.app.ports.output.yolo_base_weights_port import YoloBaseWeightsPort
from vision.app.ports.output.yolo_train_device_port import YoloTrainDevicePort
from vision.app.ports.output.yolo_train_run_port import YoloTrainRunPort
from vision.app.use_cases.detect_face_interactor import DetectFaceInteractor
from vision.app.use_cases.train_yolo_interactor import TrainYoloInteractor

_dataset_singleton: FaceDatasetPort | None = None
_train_run_singleton: YoloTrainRunPort | None = None
_base_weights_singleton: YoloBaseWeightsPort | None = None
_device_singleton: YoloTrainDevicePort | None = None
_checkpoint_singleton: FaceModelCheckpointPort | None = None
_train_yolo_singleton: TrainYoloUseCase | None = None


def get_face_dataset_port() -> FaceDatasetPort:
    global _dataset_singleton
    if _dataset_singleton is None:
        _dataset_singleton = LocalYoloFaceDatasetAdapter()
    return _dataset_singleton


def get_yolo_train_run_port() -> YoloTrainRunPort:
    global _train_run_singleton
    if _train_run_singleton is None:
        _train_run_singleton = LocalYoloTrainRunAdapter()
    return _train_run_singleton


def get_yolo_base_weights_port() -> YoloBaseWeightsPort:
    global _base_weights_singleton
    if _base_weights_singleton is None:
        _base_weights_singleton = LocalYoloBaseWeightsAdapter()
    return _base_weights_singleton


def get_yolo_train_device_port() -> YoloTrainDevicePort:
    global _device_singleton
    if _device_singleton is None:
        _device_singleton = LocalYoloTrainDeviceAdapter()
    return _device_singleton


def get_face_model_checkpoint_port() -> FaceModelCheckpointPort:
    global _checkpoint_singleton
    if _checkpoint_singleton is None:
        _checkpoint_singleton = LocalFaceModelCheckpointAdapter()
    return _checkpoint_singleton


def get_train_yolo_use_case() -> TrainYoloUseCase:
    global _train_yolo_singleton
    if _train_yolo_singleton is None:
        _train_yolo_singleton = TrainYoloInteractor(
            dataset_port=get_face_dataset_port(),
            train_run_port=get_yolo_train_run_port(),
            base_weights_port=get_yolo_base_weights_port(),
            device_port=get_yolo_train_device_port(),
        )
    return _train_yolo_singleton


def get_train_face_detector_interactor() -> TrainYoloUseCase:
    """하위 호환 — TrainYoloInteractor와 동일."""
    return get_train_yolo_use_case()


def get_detect_face_interactor() -> DetectFaceInteractor:
    return DetectFaceInteractor(checkpoint_port=get_face_model_checkpoint_port())
