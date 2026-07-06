---
tags:
  - harness/claude-sherlock-holmes
graph-group: claude-sherlock-holmes
---

# Sherlock Holmes App — CLAUDE.md

`backend/apps/sherlock_holmes/` — Titanic과 동일한 Hexagonal + Vertical Slice.

> **Import:** `from sherlock_holmes.adapter...` (`PYTHONPATH=apps`)

## 캐릭터 (introduce_myself)

| stem | prefix | 역할 |
|------|--------|------|
| `detective_sherlock_holmes` | `/sherlock/holmes` | 추론·단서 분석 |
| `doctor_watson_chronicler` | `/sherlock/watson` | 동반자·기록 |
| `inspector_lestrade_official` | `/sherlock/lestrade` | 공식 수사 |
| `mrs_hudson_housekeeper` | `/sherlock/hudson` | 하우스키퍼 |
| `brother_mycroft_strategist` | `/sherlock/mycroft` | 전략·정보 |
| `professor_moriarty_rival` | `/sherlock/moriarty` | 적대 검증 |

각 캐릭터: `GET /sherlock/{name}/myself` → `{ id, name }`.

## 슬라이스 파일 세트

`{stem}_router.py` 기준으로 schema, dto, ports, interactor, provider, pg repository가 동일 stem으로 쌍을 이룹니다.

## References

- Titanic 아키텍처: [`../titanic/_docs/structure.md`](../titanic/_docs/structure.md)
