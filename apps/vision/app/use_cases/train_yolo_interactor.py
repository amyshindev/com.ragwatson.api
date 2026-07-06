from __future__ import annotations

import logging
from pathlib import Path

from vision.app.dtos.yolo_train_dto import YoloTrainHyperparams, YoloTrainResult
from vision.app.ports.input.train_yolo_use_case import TrainYoloUseCase
from vision.app.ports.output.face_dataset_port import FaceDatasetPort
from vision.app.ports.output.yolo_base_weights_port import YoloBaseWeightsPort
from vision.app.ports.output.yolo_train_device_port import YoloTrainDevicePort
from vision.app.ports.output.yolo_train_run_port import YoloTrainRunPort

log = logging.getLogger(__name__)


class TrainYoloInteractor(TrainYoloUseCase):
    """
    YOLOv11 Nano(yolo11n.pt) 비전 훈련 오케스트레이터.

    - 데이터셋 출처(로컬/S3)는 FaceDatasetPort 구현체에만 존재
    - 산출물 저장 위치는 YoloTrainRunPort 구현체에만 존재
    - 이 클래스는 ultralytics.train() 호출만 담당
    """

    def __init__(
        self,
        dataset_port: FaceDatasetPort,
        train_run_port: YoloTrainRunPort,
        base_weights_port: YoloBaseWeightsPort,
        device_port: YoloTrainDevicePort,
    ) -> None:
        self._dataset_port = dataset_port
        self._train_run_port = train_run_port
        self._base_weights_port = base_weights_port
        self._device_port = device_port

    def execute(
        self,
        hyperparams: YoloTrainHyperparams | None = None,
        *,
        force_prepare: bool = False,
    ) -> YoloTrainResult:
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError(
                'ultralytics가 필요합니다. pip install "ultralytics>=8.3.0"',
            ) from exc

        params = hyperparams or YoloTrainHyperparams()
        manifest = self._dataset_port.prepare_dataset(force=force_prepare)
        dataset_yaml = manifest.yaml_path
        base_weights = self._base_weights_port.resolve(params.base_weights)
        device = self._device_port.resolve(params.device)

        self._train_run_port.ensure_project_directory()
        project_dir = self._train_run_port.get_project_directory()

        log.info(
            "[TrainYoloInteractor] yolo11n train yaml=%s weights=%s device=%s epochs=%s project=%s",
            dataset_yaml,
            base_weights,
            device,
            params.epochs,
            project_dir,
        )

        model = YOLO(base_weights)
        train_result = model.train(
            data=dataset_yaml,
            epochs=params.epochs,
            batch=params.batch_size,
            imgsz=params.imgsz,
            device=device,
            project=project_dir,
            name=params.run_name,
            verbose=False,
        )

        save_dir = str(getattr(train_result, "save_dir", "") or "")
        weights_path = str(Path(save_dir) / "weights" / "best.pt") if save_dir else None
        if weights_path and not Path(weights_path).is_file():
            weights_path = None

        return YoloTrainResult(
            ok=True,
            dataset_yaml=dataset_yaml,
            base_weights=base_weights,
            weights_path=weights_path,
            save_dir=save_dir or None,
            message=(
                f"YOLOv11 Nano 학습 완료 (train={manifest.train_images}, "
                f"val={manifest.val_images}, classes={len(manifest.class_names)})"
            ),
        )
