# adapter/outbound/client/n8n_client.py

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class N8nClient:
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    async def send_event(self, payload: dict[str, Any]) -> bool:
        """
        FastAPI에서 발생한 데이터를 n8n의 Webhook으로 전송합니다.
        (스타 토폴로지의 중심에서 바깥으로 뻗어나가는 통신)
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.webhook_url, json=payload)
                return response.status_code == 200
            except Exception as e:
                logger.exception("n8n 전송 실패: %s", e)
                return False
