from __future__ import annotations

from automata.adapter.outbound.client.n8n_client import N8nClient
from automata.app.dtos.ford_director_dto import FordDirectorQuery, FordDirectorResponse
from automata.app.ports.output.ford_director_port import FordDirectorPort


class FordDirectorN8nRepository(FordDirectorPort):
    def __init__(self, webhook_url: str) -> None:
        self._client = N8nClient(webhook_url)

    async def introduce_myself(self, query: FordDirectorQuery) -> FordDirectorResponse:
        return FordDirectorResponse(
            id=query.id,
            name=query.name,
            role="n8n workflow director",
        )

    async def trigger_workflow(self, query: FordDirectorQuery) -> FordDirectorResponse:
        body = {
            "workflow": query.workflow,
            "payload": query.payload,
        }
        ok = await self._client.send_event(body)
        return FordDirectorResponse(
            id=query.id,
            name=query.name,
            role="n8n workflow director",
            triggered=ok.ok,
            workflow=query.workflow,
        )
