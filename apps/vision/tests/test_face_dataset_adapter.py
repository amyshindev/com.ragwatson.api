"""YOLO 얼굴 데이터셋 준비 및 파이프라인 테스트."""

from __future__ import annotations

from pathlib import Path

import pytest

from vision.adapter.outbound.detection.local_yolo_face_dataset_adapter import (
    LocalYoloFaceDatasetAdapter,
)
from vision.app.constants.vision_paths import YOLO_TRAIN_RAW_DIR
from vision.app.ports.output.face_dataset_port import FaceDatasetPort


@pytest.fixture
def face_dataset_port(tmp_path: Path) -> FaceDatasetPort:
    prepared_root = tmp_path / "prepared_face_yolo"
    return LocalYoloFaceDatasetAdapter(raw_root=YOLO_TRAIN_RAW_DIR, prepared_root=prepared_root)


def test_prepare_yolo_face_dataset(face_dataset_port: FaceDatasetPort) -> None:
    manifest = face_dataset_port.prepare_dataset(force=True)

    assert Path(manifest.yaml_path).is_file()
    assert manifest.train_images > 0
    assert manifest.val_images > 0
    assert len(manifest.class_names) == 5
    assert "ben_afflek" in manifest.class_names

    yaml_text = Path(manifest.yaml_path).read_text(encoding="utf-8")
    assert "images/train" in yaml_text
    assert "ben_afflek" in yaml_text

    label_files = list(Path(manifest.prepared_root).glob("labels/train/*.txt"))
    assert label_files
    first_label = label_files[0].read_text(encoding="utf-8").strip().split()
    assert len(first_label) == 5
    assert float(first_label[1]) <= 1.0


def test_get_dataset_config_path(face_dataset_port: FaceDatasetPort) -> None:
    path = face_dataset_port.get_dataset_config_path(force_prepare=True)
    assert path.endswith("data.yaml")
    assert Path(path).is_file()
