import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_env_loaded = False


def _ensure_env_loaded() -> None:
    global _env_loaded
    if _env_loaded:
        return
    here = Path(__file__).resolve().parent
    for directory in [here, *here.parents]:
        candidate = directory / ".env"
        if candidate.is_file():
            load_dotenv(candidate)
            _env_loaded = True
            return
    load_dotenv()
    _env_loaded = True


def is_database_configured() -> bool:
    _ensure_env_loaded()
    return bool(os.getenv("DATABASE_URL", "").strip())


def get_database_url() -> str:
    """Return SQLAlchemy async URL for Neon PostgreSQL (psycopg async)."""
    _ensure_env_loaded()
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    if url.startswith("postgresql+psycopg://"):
        return url.replace("postgresql+psycopg://", "postgresql+psycopg_async://", 1)
    if url.startswith("postgresql://"):
        return "postgresql+psycopg_async://" + url.removeprefix("postgresql://")
    return url


@dataclass(frozen=True)
class VisionS3Settings:
    bucket: str
    region: str
    prefix: str
    access_key_id: str | None
    secret_access_key: str | None


def is_vision_s3_configured() -> bool:
    _ensure_env_loaded()
    bucket = (os.getenv("VISION_S3_BUCKET") or os.getenv("AWS_S3_BUCKET") or "").strip()
    return bool(bucket)


def get_vision_s3_settings() -> VisionS3Settings:
    _ensure_env_loaded()
    bucket = (os.getenv("VISION_S3_BUCKET") or os.getenv("AWS_S3_BUCKET") or "").strip()
    if not bucket:
        raise RuntimeError(
            "VISION_S3_BUCKET 또는 AWS_S3_BUCKET 환경 변수를 backend/.env에 설정하세요.",
        )
    return VisionS3Settings(
        bucket=bucket,
        region=(
            os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "ap-northeast-2"
        ).strip(),
        prefix=(os.getenv("VISION_S3_PREFIX") or "vision/uploads").strip().strip("/"),
        access_key_id=(os.getenv("AWS_ACCESS_KEY_ID") or "").strip() or None,
        secret_access_key=(os.getenv("AWS_SECRET_ACCESS_KEY") or "").strip() or None,
    )
