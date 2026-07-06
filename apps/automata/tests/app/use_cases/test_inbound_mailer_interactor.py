"""Tests for inbound mail receive."""

from automata.adapter.inbound.api.schemas.inbound_mailer_schema import InboundMailReceiveSchema
from automata.adapter.outbound.memory.inbound_mail_memory_repository import (
    InboundMailMemoryRepository,
)
from automata.app.use_cases.inbound_mailer_interactor import InboundMailerInteractor


async def test_receive_mail_parses_from_header() -> None:
    repo = InboundMailMemoryRepository()
    interactor = InboundMailerInteractor(repository=repo)

    result = await interactor.receive_mail(
        InboundMailReceiveSchema.model_validate(
            {
                "from": "김철수 <kim@example.com>",
                "subject": "안녕",
                "body": "테스트 본문",
            },
        ),
    )

    assert result.ok is True
    assert result.duplicate is False
    listed = await interactor.list_mails(page=1, page_size=10)
    assert listed.total == 1
    assert listed.items[0].from_email == "kim@example.com"


async def test_receive_mail_skips_duplicate_message_id() -> None:
    repo = InboundMailMemoryRepository()
    interactor = InboundMailerInteractor(repository=repo)
    payload = InboundMailReceiveSchema.model_validate(
        {
            "message_id": "msg-001",
            "from": "dup@example.com",
            "subject": "중복",
            "body": "본문",
        },
    )

    first = await interactor.receive_mail(payload)
    second = await interactor.receive_mail(payload)

    assert first.duplicate is False
    assert second.duplicate is True
    listed = await interactor.list_mails(page=1, page_size=10)
    assert listed.total == 1
