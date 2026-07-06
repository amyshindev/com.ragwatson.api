from __future__ import annotations

import logging

from vision.app.dtos.face_train_dto import FaceDetectResult, FaceDetectionBox
from vision.app.ports.output.face_model_checkpoint_port import FaceModelCheckpointPort

log = logging.getLogger(__name__)


class DetectFaceInteractor:
    """학습된 YOLO 가중치로 얼굴(유명인 클래스)을 탐지합니다."""

    def __init__(self, checkpoint_port: FaceModelCheckpointPort) -> None:
        self._checkpoint_port = checkpoint_port

    def execute(
        self,
        image_source: str,
        *,
        weights_path: str | None = None,
        confidence: float = 0.25,
    ) -> FaceDetectResult:
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError(
                'ultralytics가 필요합니다. pip install "ultralytics>=8.3.0"',
            ) from exc

        resolved_weights = self._checkpoint_port.resolve_weights_path(weights_path)
        log.info(
            "[DetectFaceInteractor] predict source=%s weights=%s",
            image_source,
            resolved_weights,
        )

        model = YOLO(resolved_weights)
        results = model.predict(source=image_source, conf=confidence, verbose=False)
        if not results:
            return FaceDetectResult(
                source=image_source,
                detections=(),
                weights_path=resolved_weights,
            )

        result = results[0]
        names = result.names or {}
        boxes: list[FaceDetectionBox] = []

        if result.boxes is not None:
            for box in result.boxes:
                cls_id = int(box.cls.item())
                conf = float(box.conf.item())
                x1, y1, x2, y2 = (float(v) for v in box.xyxy[0].tolist())
                boxes.append(
                    FaceDetectionBox(
                        class_id=cls_id,
                        class_name=str(names.get(cls_id, str(cls_id))),
                        confidence=conf,
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                    ),
                )

        return FaceDetectResult(
            source=image_source,
            detections=tuple(boxes),
            weights_path=resolved_weights,
        )
