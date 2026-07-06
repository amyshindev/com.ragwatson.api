from __future__ import annotations

import logging
from pathlib import Path

from vision.adapter.outbound.detection.yolo_face_dataset_preparer import YoloFaceDatasetPreparer
from vision.app.constants.vision_paths import PREPARED_FACE_YOLO_DIR, YOLO_TRAIN_RAW_DIR
from vision.app.ports.output.face_dataset_port import FaceDatasetManifest, FaceDatasetPort

log = logging.getLogger(__name__)


class LocalYoloFaceDatasetAdapter(FaceDatasetPort):
    """로컬 yolo_train → prepared_face_yolo data.yaml 경로를 제공합니다."""

    def __init__(
        self,
        *,
        raw_root: Path | str | None = None,
        prepared_root: Path | str | None = None,
    ) -> None:
        self._raw_root = Path(raw_root or YOLO_TRAIN_RAW_DIR)
        self._prepared_root = Path(prepared_root or PREPARED_FACE_YOLO_DIR)
        self._preparer = YoloFaceDatasetPreparer(
            raw_root=self._raw_root,
            prepared_root=self._prepared_root,
        )

    def prepare_dataset(self, *, force: bool = False) -> FaceDatasetManifest:
        log.info(
            "[LocalYoloFaceDatasetAdapter] prepare raw=%s prepared=%s force=%s",
            self._raw_root,
            self._prepared_root,
            force,
        )
        payload = self._preparer.prepare(force=force)
        return self._to_manifest(payload)

    def get_dataset_config_path(self, *, force_prepare: bool = False) -> str:
        manifest = self.prepare_dataset(force=force_prepare)
        return manifest.yaml_path

    @staticmethod
    def _to_manifest(payload: dict[str, object]) -> FaceDatasetManifest:
        class_names = payload.get("class_names") or ()
        return FaceDatasetManifest(
            yaml_path=str(payload["yaml_path"]),
            prepared_root=str(payload["prepared_root"]),
            raw_root=str(payload["raw_root"]),
            class_names=tuple(class_names),
            train_images=int(payload.get("train_images") or 0),
            val_images=int(payload.get("val_images") or 0),
        )
