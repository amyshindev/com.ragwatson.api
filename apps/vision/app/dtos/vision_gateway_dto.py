from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VisionUploadCommand:
    filename: str
    content_type: str
    size_bytes: int
    data: bytes


@dataclass(frozen=True)
class VisionUploadResult:
    file_id: str
    filename: str
    content_type: str
    size_bytes: int
    uploaded_at: str
    storage: str = "memory"
