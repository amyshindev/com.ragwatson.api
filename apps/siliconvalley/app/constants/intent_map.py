from __future__ import annotations

INTENT_MAP: dict[str, set[str]] = {
    "METRICS": {"지표", "대시", "대시보드", "매출", "성장", "mau", "dau"},
    "INFRA": {"서버", "시스템", "인프라", "배포", "장애", "log"},
    "OPERATIONS": {"운영", "프로세스", "일정", "coo", "실행"},
    "HR": {"인사", "채용", "hr", "팀", "조직"},
    "STRATEGY": {"전략", "ceo", "비전", "피치", "투자", "런웨이"},
}
