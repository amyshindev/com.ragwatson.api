from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class N8nSendResult:
    ok: bool
    status_code: int
    body: dict[str, Any] | list[Any] | str | None = None


class N8nClient:
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    async def send_event(self, payload: dict[str, Any]) -> N8nSendResult:
        """POST event payload to an n8n Webhook trigger."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.webhook_url, json=payload, timeout=60.0)
                parsed: dict[str, Any] | list[Any] | str | None
                try:
                    parsed = response.json()
                except Exception:
                    parsed = response.text or None
                return N8nSendResult(
                    ok=response.status_code == 200,
                    status_code=response.status_code,
                    body=parsed,
                )
            except Exception:
                logger.exception("n8n webhook failed url=%s", self.webhook_url)
                return N8nSendResult(ok=False, status_code=0, body=None)
