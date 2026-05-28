"""DB 연결 설정 (.env의 DATABASE_URL)."""

import os
from pathlib import Path

from dotenv import load_dotenv

_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.is_file():
    load_dotenv(_env_path)


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "").strip()


settings = Settings()
