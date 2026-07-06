"""YOLO 얼굴 학습 파이프라인 CLI (Inbound Trigger)."""

from __future__ import annotations

import argparse
import logging
import sys

from vision.app.constants.yolo_models import DEFAULT_YOLO_NANO_WEIGHTS, YOLOV8_NANO_WEIGHTS
from vision.app.dtos.yolo_train_dto import YoloTrainHyperparams
from vision.app.ports.input.train_yolo_use_case import TrainYoloUseCase
from vision.dependencies.face_detector_train_provider import (
    get_detect_face_interactor,
    get_face_dataset_port,
    get_train_yolo_use_case,
)

log = logging.getLogger(__name__)


def run_prepare_only(*, force: bool = False) -> None:
    manifest = get_face_dataset_port().prepare_dataset(force=force)
    print("=== Face dataset prepared ===")
    print(f"yaml       : {manifest.yaml_path}")
    print(f"classes    : {', '.join(manifest.class_names)}")
    print(f"train/val  : {manifest.train_images} / {manifest.val_images}")


def run_training(args: argparse.Namespace) -> None:
    trainer = get_train_yolo_use_case()
    result = trainer.execute(
        YoloTrainHyperparams(
            base_weights=args.weights,
            epochs=args.epochs,
            batch_size=args.batch,
            imgsz=args.imgsz,
            device=args.device,
            run_name=args.run_name,
        ),
        force_prepare=args.force_prepare,
    )
    print("=== Face training finished ===")
    print(f"dataset_yaml : {result.dataset_yaml}")
    print(f"weights_path : {result.weights_path}")
    print(f"save_dir     : {result.save_dir}")
    print(f"message      : {result.message}")


def run_detect(args: argparse.Namespace) -> None:
    detector = get_detect_face_interactor()
    result = detector.execute(
        args.image,
        weights_path=args.weights,
        confidence=args.confidence,
    )
    print("=== Face detection ===")
    print(f"source  : {result.source}")
    print(f"weights : {result.weights_path}")
    for i, box in enumerate(result.detections, start=1):
        print(
            f"  {i}. {box.class_name} ({box.confidence:.2f}) "
            f"[{box.x1:.0f},{box.y1:.0f},{box.x2:.0f},{box.y2:.0f}]",
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Vision YOLO face train/detect CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare_parser = sub.add_parser("prepare", help="yolo_train → YOLO data.yaml 생성")
    prepare_parser.add_argument("--force", action="store_true")

    train_parser = sub.add_parser("train", help="얼굴 YOLO 파인튜닝")
    train_parser.add_argument("--epochs", type=int, default=10)
    train_parser.add_argument("--batch", type=int, default=8)
    train_parser.add_argument("--imgsz", type=int, default=640)
    train_parser.add_argument("--device", default="auto", help="auto | cpu | 0 | cuda | mps")
    train_parser.add_argument(
        "--weights",
        default=DEFAULT_YOLO_NANO_WEIGHTS,
        help=f"기본 {DEFAULT_YOLO_NANO_WEIGHTS}, 대안 {YOLOV8_NANO_WEIGHTS}",
    )
    train_parser.add_argument("--run-name", default="train")
    train_parser.add_argument("--force-prepare", action="store_true")

    detect_parser = sub.add_parser("detect", help="학습된 모델로 얼굴 인식")
    detect_parser.add_argument("image", help="이미지 경로 또는 URL")
    detect_parser.add_argument("--weights", default=None)
    detect_parser.add_argument("--confidence", type=float, default=0.25)

    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    try:
        if args.command == "prepare":
            run_prepare_only(force=args.force)
        elif args.command == "train":
            run_training(args)
        elif args.command == "detect":
            run_detect(args)
    except Exception as exc:
        log.error("%s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
