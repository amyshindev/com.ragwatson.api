from __future__ import annotations

from typing import Any

from automata.adapter.outbound.client.n8n_client import N8nClient
from automata.app.ports.output.faker_mailer_port import (
    FakerMailerPort,
    GmailSendCommand,
    GmailSendResult,
)


class FakerMailerN8nRepository(FakerMailerPort):
    def __init__(self, webhook_url: str) -> None:
        self._client = N8nClient(webhook_url)

    async def send_gmail(self, command: GmailSendCommand) -> GmailSendResult:
        payload = {
            "workflow": "gmail-send",
            "to": command.to,
            "subject": command.subject,
            "body": command.body,
            "body_html": command.body_html or command.body,
        }
        result = await self._client.send_event(payload)
        status = "sent" if result.ok else f"failed:{result.status_code}"
        detail: dict[str, Any] | None = None
        if isinstance(result.body, dict):
            detail = result.body
        return GmailSendResult(ok=result.ok, status=status, detail=detail)
