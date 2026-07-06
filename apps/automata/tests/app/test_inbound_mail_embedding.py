"""Tests for inbound mail embedding helpers."""

from automata.adapter.outbound.ollama.inbound_mail_embedding_adapter import (
    build_mail_embedding_text,
)


def test_build_mail_embedding_text_joins_sender_subject_body() -> None:
    text = build_mail_embedding_text(
        from_email="kim@example.com",
        from_name="김철수",
        subject="안녕하세요",
        body="본문입니다.",
    )
    assert "From: 김철수" in text
    assert "Subject: 안녕하세요" in text
    assert "본문입니다." in text
