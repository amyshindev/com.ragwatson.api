---
tags:
  - harness/claude-ontology
graph-group: claude-ontology
---

# Ontology App — CLAUDE.md

이메일 스팸·피싱·프로모 분류 온톨로지 스포크 앱.

## API

| Method | Path | 설명 |
|--------|------|------|
| GET | `/ontology/spam/myself` | 분류기 소개 |
| POST | `/ontology/spam/classify` | 이메일 스팸 분류 |

### `POST /ontology/spam/classify`

```json
{
  "sender": "optional@example.com",
  "subject": "메일 제목",
  "body": "메일 본문"
}
```

응답: `{ label, score, is_blocked, reasons, matched_concepts, source }`

라벨: `ham` | `spam` | `phishing` | `promo`

## 레이어

```text
domain/ontologies/spam_taxonomy.py   개념·키워드 체계
domain/services/spam_heuristics.py   순수 규칙 엔진
adapter/outbound/neo4j/              Neo4j 그래프 enrich (선택)
adapter/outbound/memory/             Neo4j 없을 때 in-memory
app/use_cases/spam_classifier_interactor.py
core/graph/neo4j_driver.py           공용 Neo4j 드라이버
```

## automata 연동

`automata` `faker_mailer`는 발송 전 `SpamGuardPort` → ontology 분류를 호출한다.  
`is_blocked=true`이면 HTTP 422로 Gmail 발송을 차단한다.

## 환경 변수

| 변수 | 용도 |
|------|------|
| `NEO4J_URI` | 설정 시 Neo4j 온톨로지 enrich |
| `NEO4J_USER` / `NEO4J_PASSWORD` | Neo4j 인증 |

Neo4j 미설정 시 in-memory taxonomy만 사용한다.
