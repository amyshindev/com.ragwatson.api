"""TrainYoloInteractor 단위 테스트 — ultralytics 없이 Port mock."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

from vision.app.dtos.yolo_train_dto import YoloTrainHyperparams
from vision.app.ports.output.face_dataset_port import FaceDatasetManifest
from vision.app.use_cases.train_yolo_interactor import TrainYoloInteractor


@pytest.fixture
def manifest() -> FaceDatasetManifest:
    return FaceDatasetManifest(
        yaml_path="/tmp/data.yaml",
        prepared_root="/tmp/prepared",
        raw_root="/tmp/raw",
        class_names=("ben_afflek", "madonna"),
        train_images=10,
        val_images=2,
    )


def test_train_yolo_interactor_uses_ports_only(manifest: FaceDatasetManifest) -> None:
    dataset_port = MagicMock()
    dataset_port.prepare_dataset.return_value = manifest

    train_run_port = MagicMock()
    train_run_port.get_project_directory.return_value = "/tmp/runs/face_detect"

    base_weights_port = MagicMock()
    base_weights_port.resolve.return_value = "yolo11n.pt"

    device_port = MagicMock()
    device_port.resolve.return_value = "cpu"

    fake_train_result = MagicMock(save_dir="/tmp/runs/face_detect/train")
    mock_yolo_cls = MagicMock()
    mock_yolo_cls.return_value.train.return_value = fake_train_result
    fake_ultralytics = MagicMock(YOLO=mock_yolo_cls)

    with patch.dict(sys.modules, {"ultralytics": fake_ultralytics}):
        with patch("pathlib.Path.is_file", return_value=True):
            interactor = TrainYoloInteractor(
                dataset_port=dataset_port,
                train_run_port=train_run_port,
                base_weights_port=base_weights_port,
                device_port=device_port,
            )
            result = interactor.execute(
                YoloTrainHyperparams(epochs=3, batch_size=4, device="auto"),
                force_prepare=True,
            )

    dataset_port.prepare_dataset.assert_called_once_with(force=True)
    train_run_port.ensure_project_directory.assert_called_once()
    base_weights_port.resolve.assert_called_once_with("yolo11n.pt")
    device_port.resolve.assert_called_once_with("auto")
    mock_yolo_cls.assert_called_once_with("yolo11n.pt")
    mock_yolo_cls.return_value.train.assert_called_once_with(
        data="/tmp/data.yaml",
        epochs=3,
        batch=4,
        imgsz=640,
        device="cpu",
        project="/tmp/runs/face_detect",
        name="train",
        verbose=False,
    )

    assert result.ok is True
    assert result.base_weights == "yolo11n.pt"
    assert result.dataset_yaml == "/tmp/data.yaml"
    assert result.weights_path is not None
    assert result.weights_path.replace("\\", "/").endswith("/train/weights/best.pt")
