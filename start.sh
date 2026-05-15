#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}apps"
exec python -m uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"
