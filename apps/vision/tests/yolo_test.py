"""
YOLO Hello World — Ultralytics로 샘플 이미지 객체 탐지 후 결과 창 표시.

실행 (backend 폴더):
    $env:PYTHONPATH = "apps"
    python apps/vision/tests/yolo_test.py

pytest:
    pytest apps/vision/tests/yolo_test.py -v -s
"""

from __future__ import annotations

import logging
import sys

log = logging.getLogger(__name__)

# Ultralytics 공식 샘플 이미지 (버스 + 사람)
_SAMPLE_IMAGE = "https://ultralytics.com/images/bus.jpg"
_DEFAULT_MODEL = "yolo11n.pt"


def run_yolo_hello_world(*, show_window: bool = True) -> list[str]:
    """
    YOLO nano 모델로 샘플 이미지를 추론하고, 탐지된 클래스 이름 목록을 반환합니다.
    show_window=True 이면 바운딩 박스가 그려진 결과 창을 띄웁니다.
    """
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError(
            "ultralytics가 설치되지 않았습니다. backend에서 "
            'pip install "ultralytics>=8.3.0" 실행 후 다시 시도하세요.',
        ) from exc

    log.info("YOLO Hello World — model=%s image=%s", _DEFAULT_MODEL, _SAMPLE_IMAGE)
    model = YOLO(_DEFAULT_MODEL)
    results = model.predict(source=_SAMPLE_IMAGE, verbose=False)

    if not results:
        raise RuntimeError("YOLO 추론 결과가 비어 있습니다.")

    result = results[0]
    names = result.names
    labels: list[str] = []
    if result.boxes is not None:
        for cls_id in result.boxes.cls.tolist():
            labels.append(names[int(cls_id)])

    print("=== YOLO Hello World ===")
    print(f"model     : {_DEFAULT_MODEL}")
    print(f"image     : {_SAMPLE_IMAGE}")
    print(f"detections: {len(labels)}")
    for i, label in enumerate(labels, start=1):
        print(f"  {i}. {label}")

    if show_window:
        print("\n결과 창을 닫으면 프로그램이 종료됩니다.")
        result.show()

    return labels


def test_yolo_hello_world_inference() -> None:
    """헤드리스 환경용 — 창 없이 추론만 검증."""
    labels = run_yolo_hello_world(show_window=False)
    assert len(labels) > 0, "최소 1개 이상의 객체가 탐지되어야 합니다."


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        run_yolo_hello_world(show_window=True)
    except Exception as exc:
        print(f"오류: {exc}", file=sys.stderr)
        sys.exit(1)
