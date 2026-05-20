# com.ragwatson

여러 하위 프로젝트(예: `agora/`)를 두는 워크스페이스 저장소다. 이 README는 **코드베이스 소개**와 함께, Cursor에서 에이전트 행동을 묶는 **하네스 엔지니어링** 문서로의 진입점이다.

---

## Cursor 하네스 엔지니어링

LLM 코딩에서 반복되는 실패(가정 은닉, 과설계, diff 난립, 약한 완료 기준)를 줄이기 위해, 안드레 카파시의 [관찰](https://x.com/karpathy/status/2015883857489522876)과 [Karpathy Guidelines](https://github.com/forrestchang/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md)의 의도에 맞춰 규칙을 나눈다.

| 문서 | 역할 |
|------|------|
| [`.cursorrules`](.cursorrules) | **실행 하네스.** Cursor에 주입; 구현 전 `docs/` 코딩 규칙 필수. |
| [`docs/DevOps/Backend/BACKEND_RULES.md`](../docs/DevOps/Backend/BACKEND_RULES.md) | **백엔드 구현 규칙** (레이어, DB, API). |
| [`docs/DevOps/README.md`](../docs/DevOps/README.md) | Frontend/Backend 규칙 인덱스. |
| [`CLAUDE.md`](CLAUDE.md) | **상세 지침·예시·출처.** 에이전트·사람 모두 참고. |
| [`CURSOR..md`](CURSOR..md) | **설계·점검 관점.** 하네스가 무엇을 막는지, 문서 간 관계. |

규칙을 고칠 때는 위 세 곳이 **서로 모순되지 않게** 맞춘다.

### 네 가지 원칙 (요약)

1. **구현 전 사고** — 가정·모호함·트레이드오프를 드러낸다. 불분명하면 멈추고 질문한다.
2. **단순성 우선** — 요청 밖 기능·추상화·방어 코드를 넣지 않는다.
3. **정밀한 수정** — 손댄 줄이 요청과 직결되게 한다. 무관한 데드 코드는 언급만 한다.
4. **목표 중심 실행** — 검증 가능한 성공 기준을 정하고, 만족할 때까지 루프한다.

> **트레이드오프:** 속도보다 신중함을 우선한다. 사소한 작업은 합리적으로 완화한다.

자세한 문구·체크리스트·단계별 검증 예시는 [`CURSOR..md`](CURSOR..md)와 [`CLAUDE.md`](CLAUDE.md)를 본다.

---

## 하위 프로젝트

각 디렉터리의 `README.md`를 따른다. (예: `agora/agora.tjwatson/README.md`.)
