"""Kiwi 전처리 + 로컬 Ollama 한국어 모델 통합 테스트.

실행:
    cd backend
    $env:PYTHONPATH = "apps"
    python -m pytest apps/titanic/tests/test_korean_ai.py -m ollama -v -s

사전 준비:
    1. Ollama 실행 (기본 http://127.0.0.1:11434)
    2. ollama pull anpigon/eeve-korean-10.8b
"""

from __future__ import annotations

from typing import Any

import pytest

OLLAMA_MODEL = "anpigon/eeve-korean-10.8b"


def _extract_nouns(kiwi: Any, text: str) -> list[str]:
    """kiwi.tokenize()는 Token 리스트 또는 중첩 리스트를 반환할 수 있다."""
    raw = kiwi.tokenize(text)
    tokens: list[Any] = []
    for item in raw:
        if isinstance(item, list):
            tokens.extend(item)
        else:
            tokens.append(item)
    return [t.form for t in tokens if t.tag.startswith("NN")]


def _ollama_reachable() -> bool:
    try:
        import ollama

        ollama.list()
        return True
    except Exception:
        return False


def _model_pulled(model: str) -> bool:
    try:
        import ollama

        models = ollama.list().get("models", [])
        prefix = model.split(":")[0]
        return any(m.get("model", "").startswith(prefix) for m in models)
    except Exception:
        return False


def run_korean_ai(user_text: str, *, model: str = OLLAMA_MODEL) -> str:
    from kiwipiepy import Kiwi
    import ollama

    kiwi = Kiwi()

    print("\n--- [1단계] 입력 문장 전처리 중... ---")
    spaced = kiwi.space(user_text)
    cleaned_text = spaced if isinstance(spaced, str) else "".join(spaced)
    print(f"원본 문장: {user_text}")
    print(f"정제된 문장: {cleaned_text}")

    nouns = _extract_nouns(kiwi, cleaned_text)
    print(f"추출된 핵심 명사: {nouns}")

    print("\n--- [2단계] EEVE-Korean 모델 추론 중... ---")
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": cleaned_text}],
    )
    reply = response["message"]["content"]
    print("\n--- [3단계] AI 최종 답변 ---")
    print(reply)
    return reply


@pytest.fixture(scope="module")
def kiwi():
    from kiwipiepy import Kiwi

    return Kiwi()


class TestKiwiPreprocess:
    def test_space_corrects_obvious_spacing(self, kiwi):
        raw = "자연어처리는넘흐재밌어요"
        cleaned = kiwi.space(raw)
        assert cleaned != raw
        assert " " in cleaned

    def test_tokenize_extracts_nouns(self, kiwi):
        nouns = _extract_nouns(kiwi, "올라마와 키위 라이브러리")
        assert len(nouns) >= 1


@pytest.mark.ollama
@pytest.mark.skipif(not _ollama_reachable(), reason="Ollama 서버가 실행 중이 아닙니다")
@pytest.mark.skipif(
    not _model_pulled(OLLAMA_MODEL),
    reason=f"모델이 없습니다: ollama pull {OLLAMA_MODEL}",
)
class TestKoreanAiOllama:
    def test_chat_returns_non_empty_reply(self):
        question = (
            "자연어처리는 넘흐 재밌어요. 올라마와 키위 라이브러리의 장점을 한 문장으로 요약해줘."
        )
        reply = run_korean_ai(question)
        assert isinstance(reply, str)
        assert len(reply.strip()) > 0
