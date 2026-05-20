import os
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
