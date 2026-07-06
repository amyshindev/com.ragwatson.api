from __future__ import annotations

import logging
import random
import shutil
from dataclasses import dataclass
from pathlib import Path

import yaml
from PIL import Image

log = logging.getLogger(__name__)

_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
_TRAIN_RATIO = 0.8


@dataclass(frozen=True)
class _AnnotatedSample:
    class_id: int
    class_name: str
    image_path: Path
    label_line: str


class YoloFaceDatasetPreparer:
    """yolo_train/{person}/*.jpg → YOLO detection 포맷(images + labels + data.yaml)."""

    def __init__(
        self,
        *,
        raw_root: Path,
        prepared_root: Path,
        val_ratio: float = 1.0 - _TRAIN_RATIO,
        seed: int = 42,
    ) -> None:
        self._raw_root = raw_root
        self._prepared_root = prepared_root
        self._val_ratio = val_ratio
        self._seed = seed

    def prepare(self, *, force: bool = False) -> dict[str, object]:
        yaml_path = self._prepared_root / "data.yaml"
        if not force and yaml_path.is_file():
            return self._load_existing_manifest(yaml_path)

        if force and self._prepared_root.exists():
            shutil.rmtree(self._prepared_root)

        for sub in ("images/train", "images/val", "labels/train", "labels/val"):
            (self._prepared_root / sub).mkdir(parents=True, exist_ok=True)

        class_names = sorted(
            p.name
            for p in self._raw_root.iterdir()
            if p.is_dir() and not p.name.startswith(".")
        )
        if not class_names:
            raise FileNotFoundError(f"학습용 인물 폴더가 없습니다: {self._raw_root}")

        class_to_id = {name: idx for idx, name in enumerate(class_names)}
        samples = self._collect_samples(class_to_id)
        if not samples:
            raise FileNotFoundError(f"이미지 파일이 없습니다: {self._raw_root}")

        rng = random.Random(self._seed)
        rng.shuffle(samples)
        val_count = max(1, int(len(samples) * self._val_ratio))
        val_samples = samples[:val_count]
        train_samples = samples[val_count:] or val_samples[:1]

        train_n = self._materialize_split(train_samples, split="train")
        val_n = self._materialize_split(val_samples, split="val")

        manifest = {
            "path": self._prepared_root.as_posix(),
            "train": "images/train",
            "val": "images/val",
            "nc": len(class_names),
            "names": {idx: name for idx, name in enumerate(class_names)},
        }
        yaml_path.write_text(
            yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        log.info(
            "[YoloFaceDatasetPreparer] prepared train=%s val=%s classes=%s",
            train_n,
            val_n,
            len(class_names),
        )
        return {
            "yaml_path": str(yaml_path.resolve()),
            "prepared_root": str(self._prepared_root.resolve()),
            "raw_root": str(self._raw_root.resolve()),
            "class_names": tuple(class_names),
            "train_images": train_n,
            "val_images": val_n,
        }

    def _load_existing_manifest(self, yaml_path: Path) -> dict[str, object]:
        payload = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
        names = payload.get("names") or {}
        if isinstance(names, dict):
            class_names = tuple(names[i] for i in sorted(names))
        else:
            class_names = tuple(names)
        prepared_root = Path(payload.get("path") or self._prepared_root)
        train_n = len(list((prepared_root / "images/train").glob("*")))
        val_n = len(list((prepared_root / "images/val").glob("*")))
        return {
            "yaml_path": str(yaml_path.resolve()),
            "prepared_root": str(prepared_root.resolve()),
            "raw_root": str(self._raw_root.resolve()),
            "class_names": class_names,
            "train_images": train_n,
            "val_images": val_n,
        }

    def _collect_samples(self, class_to_id: dict[str, int]) -> list[_AnnotatedSample]:
        items: list[_AnnotatedSample] = []
        for class_name, class_id in class_to_id.items():
            person_dir = self._raw_root / class_name
            for image_path in sorted(person_dir.iterdir()):
                if image_path.suffix.lower() not in _IMAGE_SUFFIXES:
                    continue
                label_line = self._annotate_face(class_id, image_path)
                if label_line is None:
                    continue
                items.append(
                    _AnnotatedSample(
                        class_id=class_id,
                        class_name=class_name,
                        image_path=image_path,
                        label_line=label_line,
                    ),
                )
        return items

    def _annotate_face(self, class_id: int, image_path: Path) -> str | None:
        try:
            with Image.open(image_path) as image:
                width, height = image.size
        except OSError:
            log.warning("이미지를 읽을 수 없습니다: %s", image_path)
            return None

        x, y, w, h = self._fallback_face_box(width, height)
        x_c, y_c, bw, bh = self._to_yolo_norm((float(x), float(y), float(w), float(h)), width, height)
        return f"{class_id} {x_c:.6f} {y_c:.6f} {bw:.6f} {bh:.6f}"

    @staticmethod
    def _fallback_face_box(width: int, height: int) -> tuple[float, float, float, float]:
        side = min(width, height) * 0.75
        x = (width - side) / 2
        y = (height - side) / 2
        return x, y, side, side

    @staticmethod
    def _to_yolo_norm(
        box: tuple[float, float, float, float],
        width: int,
        height: int,
    ) -> tuple[float, float, float, float]:
        x, y, w, h = box
        x_c = (x + w / 2) / width
        y_c = (y + h / 2) / height
        return x_c, y_c, w / width, h / height

    def _materialize_split(self, samples: list[_AnnotatedSample], *, split: str) -> int:
        count = 0
        for idx, sample in enumerate(samples):
            stem = f"{sample.class_name}_{idx:04d}"
            dest_image = self._prepared_root / "images" / split / f"{stem}{sample.image_path.suffix.lower()}"
            dest_label = self._prepared_root / "labels" / split / f"{stem}.txt"
            shutil.copy2(sample.image_path, dest_image)
            dest_label.write_text(sample.label_line + "\n", encoding="utf-8")
            count += 1
        return count
