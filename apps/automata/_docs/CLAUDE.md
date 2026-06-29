---
tags:
  - harness/claude-automata
graph-group: claude-automata
---

# Automata App — CLAUDE.md

n8n 업무 자동화 도메인. `star_craft` 허브에서 라우팅된 이벤트를 n8n 웹훅으로 전달한다.

## 캐릭터

| 캐릭터 | 모듈 stem | 역할 |
|--------|-----------|------|
| **Ford (Director)** | `ford_director` | n8n 워크플로우 트리거·오케스트레이션 |
| **Faker (Mailer)** | `faker_mailer` | ExaONE 초안 작성 + Gmail n8n 발송 |

## API

| Method | Path | 설명 |
|--------|------|------|
| GET | `/automata/ford/myself` | Ford 디렉터 소개 |
| POST | `/automata/ford/trigger` | n8n 웹훅으로 이벤트 전송 |
| POST | `/automata/faker/email` | ExaONE 메일 초안 + n8n Gmail 발송 |

### `POST /automata/faker/email`

요청:

```json
{
  "to": "recipient@example.com",
  "prompt": "메일 작성 지시",
  "subject": "선택"
}
```

응답: `{ ok, to, subject, body_preview, n8n_status }`

## 환경 변수

| 변수 | 예시 |
|------|------|
| `N8N_WEBHOOK_URL` | `http://n8n:5678/webhook/automata` (Docker) |
| `OLLAMA_BASE_URL` | `http://host.docker.internal:11434` (Docker → 호스트 Ollama) |
| `EXAONE_MODEL` | `exaone3.5:2.4b` |

## n8n Gmail 워크플로

- Import: `n8n/workflows/automata-gmail.json`
- 설정: `n8n/workflows/README.md`
- 페이로드 `workflow: gmail-send` + `to`, `subject`, `body`

## 레이어

```text
adapter/inbound/api/v1/ford_director_router.py
adapter/inbound/api/v1/faker_mailer_router.py
adapter/outbound/n8n/ford_director_n8n_repository.py
adapter/outbound/n8n/faker_mailer_n8n_repository.py
adapter/outbound/client/n8n_client.py
app/use_cases/ford_director_interactor.py
app/use_cases/faker_mailer_interactor.py
dependencies/ford_director_provider.py
dependencies/faker_mailer_provider.py
core/lol/t1_mid_faker_orchestrator.py  (ExaONE, shared)
```

## 프론트엔드

- `frontend/lib/automata-api.ts` — `sendFakerEmail()`
- `frontend/app/automata/page.tsx` — 발송 폼
