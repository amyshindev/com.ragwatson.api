---
tags:
  - harness/claude-backend
graph-group: claude-backend
---

# Backend — CLAUDE.md

FastAPI / Python scope for `backend/`. Inherits the repository blueprint from [`../CLAUDE.md`](../CLAUDE.md).

> **Precedence:** [`../CLAUDE.md`](../CLAUDE.md) on structure and layering · [`docs/DevOps/Backend/BACKEND_RULES.md`](../docs/DevOps/Backend/BACKEND_RULES.md) on implementation detail · this file on **backend layout and app siblings**.

---

## 1. Before You Code

1. Read [`../CLAUDE.md`](../CLAUDE.md) (blueprint + agent behavior).
2. Read [`docs/DevOps/Backend/BACKEND_RULES.md`](../docs/DevOps/Backend/BACKEND_RULES.md) for layers, DB, API, logging.
3. If the task is inside a domain app, read that app's `.docs/CLAUDE.md` (e.g. [`apps/titanic/_docs/CLAUDE.md`](apps/titanic/_docs/CLAUDE.md)).

---

## 2. Runtime Layout

| Item | Rule |
|------|------|
| App root | `backend/apps/` (`PYTHONPATH=apps`) |
| Entry | `backend/main.py` → `uvicorn main:app` |
| Local run | `backend/start-backend.ps1` (port **8000**) |
| Env | `backend/.env` (via `core.matrix.keymaker` bootstrap) |
| Secrets | Never commit `.env` or API keys |

---

## 3. Module Pathing (@backend)

---> **This section was at repository root; it is canonical here for all backend work.**

- **Root omission:** For imports under `backend/apps/`, omit `backend` and `apps` from the package path. Example: `from titanic.adapter.inbound.api import titanic_router`.
- **Core entry:** Shared infrastructure under `backend/core/` is imported as `core.*` (e.g. `core.matrix.keymaker_api`, `core.config`).
- **Cross-app:** Domain apps do not import each other's adapters; share via `core/` or explicit application boundaries.

---

## 4. Sibling Apps under `backend/apps/`

Each peer directory is an independent bounded context. New domains add a **sibling** package, not a nested subfolder of an existing app.

```text
backend/apps/
  titanic/          ← hexagonal ML + character APIs
  audio/            ← ML audio pipeline
  user/             ← auth / signup
  agora/            ← legacy / teaching modules
  board/, gallery/, library/, …
  core/             ← shared config, DB helpers (not a domain app)
```

**Per-app contract:**

| Concern | Location |
|---------|----------|
| Domain rules for agents | `apps/{app}/.docs/CLAUDE.md` |
| HTTP surface | `apps/{app}/adapter/inbound/api/` |
| Use cases | `apps/{app}/app/use_cases/` |
| Ports | `apps/{app}/app/ports/input|output/` |
| DI / FastAPI `Depends` | `apps/{app}/dependencies/` |
| ORM / PG | `apps/{app}/adapter/outbound/` |

`main.py` only **registers routers** and global middleware — no business logic.

When adding a new app, create `apps/{name}/.docs/CLAUDE.md` using the titanic file as a template.

---

## 5. Hexagonal Layers (per app)

```text
adapter/inbound/api/v1/*_router.py     → HTTP, Pydantic schemas, Depends
dependencies/*_provider.py             → wire repository + interactor
app/use_cases/*_interactor.py          → orchestration
app/ports/input/*_use_case.py          → inbound port (ABC)
app/ports/output/*_repository.py       → outbound port (ABC)
adapter/outbound/pg/*_pg_repository.py → SQLAlchemy / external I/O
domain/entities/                       → pure domain (no FastAPI / ORM)
```

**Depends rule:** Resolve dependencies in `dependencies/*_provider.py` and router `Depends(...)`. Do not put `Depends` inside interactors.

---

## 6. Database & API (summary)

Full rules: [`docs/DevOps/Backend/BACKEND_RULES.md`](../docs/DevOps/Backend/BACKEND_RULES.md).

- Async `AsyncSession`; write paths use `commit` / `rollback` at the route or transaction boundary.
- Request/response: Pydantic `BaseModel`, `response_model` on routes.
- Client errors: `HTTPException` with Korean `detail` where the codebase already does.
- Logging: `logger = logging.getLogger(__name__)`, layer completion logs when matching existing style.

---

## 7. Domain Apps — Deep Links

| App | Agent doc |
|-----|-----------|
| Titanic | [`apps/titanic/_docs/CLAUDE.md`](apps/titanic/_docs/CLAUDE.md) |
| *(future)* | `apps/{app}/.docs/CLAUDE.md` |

---

## 8. Checklist

- [ ] Logic sits in the correct layer (router → provider → interactor → repository).
- [ ] Imports use `titanic.*` / `core.*` style — not `backend.apps.*`.
- [ ] Domain `.docs/CLAUDE.md` consulted when editing that app.
- [ ] No secrets in diff; `/docs` smoke-check for new endpoints.

## References

- Root blueprint: [`../CLAUDE.md`](../CLAUDE.md)
- Implementation: [`docs/DevOps/Backend/BACKEND_RULES.md`](../docs/DevOps/Backend/BACKEND_RULES.md)
- DevOps index: [`docs/DevOps/README.md`](../docs/DevOps/README.md)
