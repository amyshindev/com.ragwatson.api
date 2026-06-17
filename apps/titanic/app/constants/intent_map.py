from __future__ import annotations

INTENT_MAP: dict[str, set[str]] = {
    "SURVIVAL_PREDICT": {
        "생존", "사망", "살", "죽", "예측", "판별", "가능", "확률",
    },
    "STATISTICS": {
        "몇", "명", "수", "통계", "전체", "탑승", "승객", "인원", "합계",
    },
    "PASSENGER_SEARCH": {
        "검색", "찾", "누구", "이름", "승객", "탑승객",
    },
    "MODEL_TRAIN": {
        "학습", "훈련", "모델", "알고리즘", "정확도", "성능", "순위", "훈련시",
    },
}
