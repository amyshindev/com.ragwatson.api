---
tags:
  - harness/claude-titanic
graph-group: claude-titanic
---

# Titanic App — CLAUDE.md

Domain rules for `backend/apps/titanic/`. Inherits:

- Repository blueprint: [`../../../../CLAUDE.md`](../../../../CLAUDE.md)
- Backend layout: [`../../../CLAUDE.md`](../../../CLAUDE.md)
- Frontend pages: [`../../../../frontend/CLAUDE.md`](../../../../frontend/CLAUDE.md)

> **Precedence:** Parent `CLAUDE.md` files on structure · this file on **Titanic personas, ML roles, and API contracts**.

---

## 1. Purpose

Teaching / demo domain: Titanic passengers and crew as **named hexagonal modules**. Each character maps to a router + interactor + repository slice. ML pipelines (CSV, survival model) are woven through character metaphors (Jack trains Rose; Smith orchestrates chat).

Sibling apps (`audio`, `user`, …) follow the same `.docs/CLAUDE.md` pattern at `backend/apps/{app}/.docs/CLAUDE.md`.

---

## 2. Naming Convention

| Prefix | Role | Examples |
|--------|------|----------|
| `crew_*` | Ship crew / officers | `crew_smith_captain`, `crew_james_director`, `crew_walter_roaster` |
| `passenger_*` | Passengers / ML roles | `passenger_rose_model`, `passenger_jack_trainer`, `passenger_ruth_validation` |

File stem repeats the prefix: `crew_smith_captain_router.py`, `passenger_rose_model_interactor.py`, etc.

---

## 3. Layer Map

```text
adapter/inbound/api/
  schemas/          ← Pydantic (model_config + json_schema_extra examples)
  v1/*_router.py    ← FastAPI routes, prefix /titanic/{character}
dependencies/
  *_provider.py     ← get_*_repository, get_*_use_case (Depends wiring)
app/
  use_cases/*_interactor.py
  ports/input/*_use_case.py
  ports/output/*_repository.py
  dtos/
adapter/outbound/
  pg/*_pg_repository.py
  orm/
domain/entities/
tests/
```

**Router registration:** `adapter/inbound/api/__init__.py` → `titanic_router` included in `main.py` **without** an extra `/api` prefix.

---

## 4. Key Characters & Responsibilities

| Character | Module stem | Responsibility |
|-----------|-------------|----------------|
| **Smith (Captain)** | `crew_smith_captain` | Orchestration; `POST /titanic/smith/chat` (Gemini persona); `GET /titanic/smith/myself` |
| **Rose** | `passenger_rose_model` | `DecisionTreeClassifier` survival model + `introduce_myself`; single `RoseModelInteractor` (ML + character) |
| **Jack (Trainer)** | `passenger_jack_trainer` | Trains Rose from `WalterReader` CSV features / fallback sample data |
| **James (Director)** | `crew_james_director` | CSV upload, passenger/booking persistence |
| **Walter (Roaster)** | `crew_walter_roaster` | Dataset read / feature extraction |
| **Others** | `passenger_*`, `crew_*` | Scaler, validation, architect, etc. — one concern per router |

### Smith chat flow

```text
POST /titanic/smith/chat  { "message": "..." }
  → crew_smith_captain_router
  → get_smith_captain_use_case (provider)
  → SmithCaptainInteractor
       __init__: jack.train_rose_model(rose)   # Rose ML warmed on wire-up
       chat(): repository.chat(ChatSchema)     # Gemini via keymaker
  → { "reply": "..." }
```

Schemas: `ChatSchema`, `ChatResponseSchema` in `crew_smith_captain_schema.py` — use `model_config.json_schema_extra.example` like `SmithCaptainSchema`.

### Rose model

- **Use:** `RoseModelInteractor` in `passenger_rose_model_interactor.py` (train / predict / introduce_myself).
- **Provider:** `get_rose_model` in `passenger_rose_model_provider.py`.
- **Not** a separate `*_train_interactor` — training lives on the same class.

---

## 5. API Prefixes (v1)

All routes hang under `/titanic/...`:

| Tag | Prefix | Notes |
|-----|--------|-------|
| smith | `/titanic/smith` | chat, myself |
| rose | `/titanic/rose` | myself |
| jack | `/titanic/jack` | trainer |
| james | `/titanic/james` | CSV / director |
| … | `/titanic/{name}` | see `adapter/inbound/api/v1/` |

---

## 6. External Services

| Service | Usage |
|---------|--------|
| **Gemini** | Smith chat (`core.matrix.keymaker`); requires `GEMINI_API_KEY` in `backend/.env` |
| **PostgreSQL** | Neon / local via async SQLAlchemy for persistence routes |
| **sklearn** | Rose `DecisionTreeClassifier` |
| **ollama / kiwipiepy** | Listed in `backend/requirements.txt` for future local LLM / Korean NLP |

---

## 7. Adding a New Titanic Character

1. Copy an existing `*_router.py` + `*_interactor.py` + `*_provider.py` triple.
2. Register router in `adapter/inbound/api/__init__.py`.
3. Add schema with `model_config` example block.
4. Extend this doc's character table if the role is stable.

---

## 8. Adding a New Sibling App (not Titanic)

Do **not** nest under `titanic/`. Add `backend/apps/{new_app}/` with the same hexagonal tree and create `backend/apps/{new_app}/.docs/CLAUDE.md`.

---

## 9. Checklist

- [ ] New code follows `crew_*` / `passenger_*` naming.
- [ ] Depends only in `dependencies/`, not inside interactors.
- [ ] Pydantic schemas include `json_schema_extra` examples where applicable.
- [ ] Router prefix is `/titanic/...` consistent with frontend `lib/titanic-api.ts`.
- [ ] Parent [`backend/CLAUDE.md`](../../../CLAUDE.md) layer rules respected.

## References

- Root: [`../../../../CLAUDE.md`](../../../../CLAUDE.md)
- Backend: [`../../../CLAUDE.md`](../../../CLAUDE.md)
- Backend rules: [`../../../../docs/DevOps/Backend/BACKEND_RULES.md`](../../../../docs/DevOps/Backend/BACKEND_RULES.md)
- Project notes (wiki): `docs/타이타닉개발/` when present in the `docs` submodule


## 타이타닉 도메인 문서 연결

* 타이타닉 도메인 문서 연결
* 타이타닉 피처 정리: [[titanic-features]]
* 타이타닉 머신러닝: [[titanic-machine_learning]]
* 타이타닉 ERD: [[TITANIC-ERD]]
* 타이타닉 NF: [[titanic-nf]]
* 타이타닉 알고리즘: [[titanic-algorithms]]
* 