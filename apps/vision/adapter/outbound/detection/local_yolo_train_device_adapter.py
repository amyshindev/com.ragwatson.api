from __future__ import annotations

import logging

from vision.app.ports.output.yolo_train_device_port import YoloTrainDevicePort

log = logging.getLogger(__name__)

_AUTO_ALIASES = frozenset({"auto", "", "default"})


class LocalYoloTrainDeviceAdapter(YoloTrainDevicePort):
    """CUDA / MPS / CPU 자동 선택 (torch.cuda.is_available 기준)."""

    def resolve(self, requested: str | int) -> str | int:
        token = str(requested).strip().lower() if not isinstance(requested, int) else requested
        if isinstance(requested, int):
            return requested
        if token not in _AUTO_ALIASES and token not in ("cpu", "cuda", "mps"):
            # "0", "1" 등 GPU 인덱스 문자열
            if token.isdigit():
                return int(token)
            return requested

        if token not in _AUTO_ALIASES:
            return requested

        try:
            import torch
        except ImportError:
            log.warning("torch 미설치 — device=cpu 사용")
            return "cpu"

        if torch.cuda.is_available():
            name = torch.cuda.get_device_name(0)
            log.info("[LocalYoloTrainDeviceAdapter] auto → cuda:0 (%s)", name)
            return 0

        mps_backend = getattr(torch.backends, "mps", None)
        if mps_backend is not None and mps_backend.is_available():
            log.info("[LocalYoloTrainDeviceAdapter] auto → mps")
            return "mps"

        log.warning(
            "[LocalYoloTrainDeviceAdapter] GPU 없음 (torch=%s) — device=cpu. "
            "CUDA PyTorch 설치: pip install torch --index-url https://download.pytorch.org/whl/cu126",
            torch.__version__,
        )
        return "cpu"
