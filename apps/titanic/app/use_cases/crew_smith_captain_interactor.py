from __future__ import annotations

import logging
import re
from typing import Any

import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    ChatSchema,
    SmithCaptainSchema,
)
from titanic.adapter.outbound.orm.passenger_rose_model_strategies import RoseModelStrategy
from titanic.app.dtos.crew_smith_captain_dto import (
    ChatResponse,
    SmithCaptainQuery,
    SmithCaptainResponse,
)
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort
from titanic.app.use_cases.passenger_jack_trainer_interactor import (
    _normalize_train_columns,
    _preprocess_train,
)
from titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor

logger = logging.getLogger(__name__)

_FEATURE_LABELS = {
    "Sex": "성별",
    "Pclass": "티켓 등급",
    "Fare": "요금",
    "Age": "나이",
    "Parch": "부모/자녀 수",
    "SibSp": "형제/배우자 수",
}

_CONFUSION_MARKERS = ("뭔소리", "무슨 말", "이해가", "이해 안", "모르겠", "왜 그래", "엉뚱")
_AGE_CONTEXT_MARKERS = ("나이", "세", "승객", "탑승", "탑승객", "승선")
_OLD_AGE_MARKERS = ("많", "높", "크", "연장", "늙", "고령", "많은")
_YOUNG_AGE_MARKERS = ("어리", "어린", "적", "작", "낮", "젊", "연소")
_SUPERLATIVE_MARKERS = ("제일", "가장", "최고", "최소", "최연", "top")


class SmithCaptainInteractor(SmithCaptainUseCase):
    def __init__(
        self,
        repository: SmithCaptainPort,
        andrews: AndrewsArchitectUseCase,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
        cal: CalTesterUseCase,
        walter: WalterRoasterUseCase,
        hartley: HartleyViolinUseCase,
    ):
        self.repository = repository
        self.andrews = andrews
        self.jack = jack
        self.rose = rose
        self.cal = cal
        self.walter = walter
        self.hartley = hartley

    def _equip_rose_with_best_model(
        self,
        algorithm_key: str,
        trained_strategies: dict[str, RoseModelStrategy],
    ) -> RoseModelInteractor:
        self.rose.set_strategy(trained_strategies[algorithm_key])
        return self.rose

    def _resolve_eval_dataframe(
        self, train_set: pd.DataFrame, test_set: pd.DataFrame
    ) -> pd.DataFrame:
        if "Survived" in test_set.columns or "survived" in test_set.columns:
            return test_set

        from sklearn.model_selection import train_test_split

        label_column = "Survived" if "Survived" in train_set.columns else "survived"
        _, eval_df = train_test_split(
            train_set,
            test_size=0.2,
            random_state=42,
            stratify=train_set[label_column],
        )
        return eval_df

    def _resolve_intent(self, message: str, question: dict[str, Any]) -> str:
        intent = question["intent"]
        if self._is_passenger_lookup_question(message):
            return "PASSENGER_SEARCH"
        if intent == "UNKNOWN" and self._is_feature_importance_question(message):
            return "FEATURE_IMPORTANCE"
        if intent == "SURVIVAL_PREDICT" and self._is_feature_importance_question(message):
            return "FEATURE_IMPORTANCE"
        return intent

    def _is_passenger_lookup_question(self, message: str) -> bool:
        if (
            self._is_oldest_age_question(message)
            or self._is_youngest_age_question(message)
            or self._is_highest_fare_question(message)
        ):
            return True
        lookup_markers = ("이름", "누구", "누가", "검색", "찾")
        context_markers = (
            "나이",
            "세",
            "탑승",
            "승객",
            "많",
            "어리",
            "어린",
            "제일",
            "가장",
            "요금",
            "비싼",
            "싼",
        )
        return any(marker in message for marker in lookup_markers) and any(
            marker in message for marker in context_markers
        )

    def _has_age_context(self, message: str) -> bool:
        return any(marker in message for marker in _AGE_CONTEXT_MARKERS)

    def _has_superlative(self, message: str) -> bool:
        return any(marker in message for marker in _SUPERLATIVE_MARKERS)

    def _is_confusion_message(self, message: str) -> bool:
        return any(marker in message for marker in _CONFUSION_MARKERS)

    def _column_series(self, df: pd.DataFrame, *candidates: str) -> pd.Series | None:
        for name in candidates:
            if name in df.columns:
                return df[name]
        return None

    def _format_passenger_brief(self, row: pd.Series) -> str:
        name = row.get("Name") or row.get("name", "알 수 없음")
        age_value = row.get("Age", row.get("age"))
        sex = str(row.get("Sex") or row.get("gender", "")).lower()
        sex_label = "남성" if sex == "male" else "여성" if sex == "female" else sex or "성별 미상"
        pclass = row.get("Pclass", row.get("pclass", "?"))
        survived = row.get("Survived", row.get("survived"))
        survived_label = ""
        if survived is not None and pd.notna(survived):
            survived_label = f", {'생존' if int(survived) == 1 else '사망'}"
        if age_value is not None and pd.notna(age_value):
            age_label = f"{float(age_value):.0f}세"
        else:
            age_label = "나이 미상"
        return f"{name} ({age_label}, {sex_label}, {pclass}등석{survived_label})"

    def _is_oldest_age_question(self, message: str) -> bool:
        if not any(marker in message for marker in _OLD_AGE_MARKERS):
            return False
        return self._has_age_context(message) or self._has_superlative(message)

    def _is_youngest_age_question(self, message: str) -> bool:
        if not any(marker in message for marker in _YOUNG_AGE_MARKERS):
            return False
        return self._has_age_context(message) or self._has_superlative(message)

    def _is_highest_fare_question(self, message: str) -> bool:
        return any(
            marker in message for marker in ("요금", "티켓", "운임", "비싼", "높은")
        ) and any(marker in message for marker in ("제일", "가장", "최고", "많", "비싼", "높"))

    def _build_passenger_search_reply(self, message: str, train_set: pd.DataFrame) -> str:
        if train_set.empty:
            return "승객 데이터를 불러오지 못했습니다."

        df = train_set.copy()
        ages = self._column_series(df, "Age", "age")
        if ages is not None:
            age_numeric = pd.to_numeric(ages, errors="coerce")
            valid_age_df = df[age_numeric.notna()].copy()
            valid_age_df["_age"] = age_numeric[age_numeric.notna()]

            if self._is_oldest_age_question(message) and not valid_age_df.empty:
                row = valid_age_df.loc[valid_age_df["_age"].idxmax()]
                return f"가장 나이가 많은 탑승객은 {self._format_passenger_brief(row)}입니다."

            if self._is_youngest_age_question(message) and not valid_age_df.empty:
                row = valid_age_df.loc[valid_age_df["_age"].idxmin()]
                return f"가장 나이가 어린 탑승객은 {self._format_passenger_brief(row)}입니다."

        fares = self._column_series(df, "Fare", "fare")
        if fares is not None and self._is_highest_fare_question(message):
            fare_numeric = pd.to_numeric(fares, errors="coerce")
            valid_fare_df = df[fare_numeric.notna()].copy()
            if not valid_fare_df.empty:
                valid_fare_df["_fare"] = fare_numeric[fare_numeric.notna()]
                row = valid_fare_df.loc[valid_fare_df["_fare"].idxmax()]
                return f"가장 높은 요금을 낸 승객은 {self._format_passenger_brief(row)}입니다."

        names = self._column_series(df, "Name", "name")
        if names is not None:
            latin_match = re.search(r"([A-Z][a-z]+)", message)
            if latin_match:
                query = latin_match.group(1)
                hits = df[names.astype(str).str.contains(query, case=False, na=False)]
                if not hits.empty:
                    lines = [
                        f"- {self._format_passenger_brief(hits.iloc[index])}"
                        for index in range(min(3, len(hits)))
                    ]
                    suffix = f" 외 {len(hits) - 3}명" if len(hits) > 3 else ""
                    return f"'{query}'(으)로 찾은 승객입니다{suffix}.\n" + "\n".join(lines)

        return (
            "승객 검색을 이해하지 못했습니다. 예: '제일 나이가 많은 승객 이름', "
            "'가장 어린 승객은 누구', 'Brock 검색'처럼 질문해 주세요."
        )

    def _is_feature_importance_question(self, message: str) -> bool:
        importance_markers = ("중요", "요인", "상관", "영향", "핵심", "결정", "무엇", "뭐")
        survival_markers = ("생존", "생존율", "변수", "피처", "요소")
        return any(marker in message for marker in importance_markers) and any(
            marker in message for marker in survival_markers
        )

    def _parse_passenger_profile(self, message: str) -> dict[str, Any]:
        profile: dict[str, Any] = {}

        age_match = re.search(r"(\d{1,3})\s*세", message)
        if age_match:
            profile["age"] = float(age_match.group(1))

        if any(word in message for word in ("여성", "여자", "female", "Female")):
            profile["gender"] = "female"
        elif any(word in message for word in ("남성", "남자", "male", "Male")):
            profile["gender"] = "male"

        if any(word in message for word in ("1등", "일등", "1등석")):
            profile["pclass"] = 1
        elif any(word in message for word in ("2등", "이등", "2등석")):
            profile["pclass"] = 2
        elif any(word in message for word in ("3등", "삼등", "3등석")):
            profile["pclass"] = 3

        return profile

    def _build_passenger_dataframe(self, profile: dict[str, Any]) -> pd.DataFrame:
        gender = profile.get("gender", "male")
        title = "Mr." if gender == "male" else "Miss."
        return pd.DataFrame(
            [
                {
                    "Survived": 0,
                    "Pclass": profile.get("pclass", 3),
                    "Name": profile.get("name", f"Guest, {title} Unknown"),
                    "Sex": gender,
                    "Age": profile.get("age", 30.0),
                    "SibSp": profile.get("sibsp", 0),
                    "Parch": profile.get("parch", 0),
                    "Fare": profile.get("fare", 7.0),
                    "Embarked": profile.get("embarked", "S"),
                }
            ]
        )

    def _preprocess_passenger_for_prediction(self, profile: dict[str, Any]) -> list[list[float]]:
        passenger = self._build_passenger_dataframe(profile)
        reference = self.walter.get_train_set().head(20)
        combined = pd.concat([passenger, reference], ignore_index=True)
        normalized = _normalize_train_columns(combined)
        features, _ = _preprocess_train(normalized)
        return features[:1]

    def _predict_passenger_survival(self, profile: dict[str, Any]) -> tuple[int, float | None]:
        features = self._preprocess_passenger_for_prediction(profile)
        prediction = self.rose.predict_strategy_rows(features)[0]
        survival_probability: float | None = None
        if self.rose._active_strategy is not None:
            probabilities = self.rose._active_strategy.predict_proba(features)
            survival_probability = float(probabilities[0]) if probabilities else None
        return prediction, survival_probability

    def _describe_passenger_profile(self, profile: dict[str, Any]) -> str:
        parts: list[str] = []
        if "age" in profile:
            parts.append(f"{profile['age']:.0f}세")
        if profile.get("gender") == "female":
            parts.append("여성")
        elif profile.get("gender") == "male":
            parts.append("남성")
        if "pclass" in profile:
            parts.append(f"{profile['pclass']}등석")
        return ", ".join(parts) if parts else "입력하신 승객"

    def _build_feature_importance_reply(self, best_model_name: str, best_accuracy: float) -> str:
        build_matrix = getattr(self.hartley, "build_correlation_matrix", None)
        if build_matrix is None:
            return (
                "생존에 가장 큰 영향을 준 변수는 성별, 티켓 등급, 요금 순입니다. "
                f"(모델: {best_model_name}, test 정확도 {best_accuracy:.2%})"
            )

        correlation = build_matrix()
        survived_column = "Survived" if "Survived" in correlation.columns else "survived"
        if survived_column not in correlation.columns:
            return "생존율 상관 분석 데이터를 찾지 못했습니다."

        ranked = (
            correlation[survived_column]
            .drop(labels=[survived_column], errors="ignore")
            .abs()
            .sort_values(ascending=False)
        )
        ranked = ranked.drop(
            labels=[
                label for label in ranked.index if str(label) in {"PassengerId", "passenger_id"}
            ],
            errors="ignore",
        )

        lines = ["생존율(`Survived`)과 상관이 큰 변수 순서입니다."]
        for index, (feature, value) in enumerate(ranked.items(), start=1):
            label = _FEATURE_LABELS.get(str(feature), str(feature))
            direction = (
                "양의 상관" if correlation.loc[feature, survived_column] >= 0 else "음의 상관"
            )
            lines.append(f"{index}. {label} (`{feature}`) → {value:.2f} ({direction})")

        lines.append(
            f"핵심은 성별·티켓 등급·요금입니다. 현재 최고 모델은 {best_model_name} "
            f"(test 정확도 {best_accuracy:.2%})입니다."
        )
        return "\n".join(lines)

    def _build_reply(
        self,
        intent: str,
        message: str,
        question: dict[str, Any],
        train_set: pd.DataFrame,
        train_result: dict[str, Any],
        test_result: dict[str, Any],
        best_model_name: str,
        best_accuracy: float,
    ) -> str:
        if intent == "FEATURE_IMPORTANCE":
            return self._build_feature_importance_reply(best_model_name, best_accuracy)

        if intent == "STATISTICS":
            return f"탑승객은 {len(train_set)}명입니다. (학습 데이터 기준)"

        if intent == "MODEL_TRAIN":
            trained_count = len(train_result.get("train_results", []))
            return (
                f"잭이 {trained_count}개 모델을 훈련했습니다. "
                f"캘 테스터 결과 {best_model_name}이(가) test 정확도 {best_accuracy:.2%}로 1위입니다."
            )

        if intent == "SURVIVAL_PREDICT":
            profile = self._parse_passenger_profile(message)
            if profile:
                prediction, survival_probability = self._predict_passenger_survival(profile)
                survived = "생존" if prediction == 1 else "사망"
                profile_text = self._describe_passenger_profile(profile)
                probability_text = (
                    f" 생존 확률은 약 {survival_probability:.1%}입니다."
                    if survival_probability is not None
                    else ""
                )
                return (
                    f"로즈({best_model_name}) 예측: {profile_text} 승객은 {survived}할 가능성이 높습니다."
                    f"{probability_text} (test 정확도 {best_accuracy:.2%})"
                )

            sample_features = test_result.get("sample_features", [])
            if sample_features:
                prediction = self.rose.predict_strategy_rows(sample_features[:1])[0]
                survived = "생존" if prediction == 1 else "사망"
                return (
                    f"로즈({best_model_name}) 예측: 해당 승객은 {survived}할 것으로 보입니다. "
                    f"(test 정확도 {best_accuracy:.2%})"
                )
            return (
                "예측할 승객 정보가 부족합니다. 예: '33세 남자라면 살 수 있었을까?'처럼 "
                f"나이와 성별을 알려주세요. (모델: {best_model_name})"
            )

        if intent == "PASSENGER_SEARCH":
            return self._build_passenger_search_reply(message, train_set)

        if self._is_confusion_message(message):
            return (
                "죄송합니다, 답이 부족했군요. 승객 수·이름 검색·생존 예측·생존 요인 등 "
                "구체적으로 다시 질문해 주시면 데이터로 답하겠습니다."
            )

        return (
            f"선장 스미스입니다. 로즈에게 장착된 최고 모델은 {best_model_name} "
            f"(test 정확도 {best_accuracy:.2%})입니다."
        )

    async def chat(self, schema: ChatSchema) -> ChatResponse:
        message = schema.message if isinstance(schema.message, str) else str(schema.message)
        logger.info("[SmithCaptainInteractor] chat 진입 | message=%s", message)

        train_set = self.walter.get_train_set()
        test_set = self.walter.get_test_set()
        train_result = await self.jack.get_model_train(train_set)
        eval_df = self._resolve_eval_dataframe(train_set, test_set)
        test_result = await self.cal.get_model_test(
            {
                "df": eval_df,
                "trained_strategies": train_result["trained_strategies"],
            }
        )
        question = self.andrews.analyze_intent(message)
        intent = self._resolve_intent(message, question)

        best_algorithm = test_result["best_algorithm"]
        best_accuracy = float(test_result["best_test_accuracy"])
        best_model_name = test_result["best_model_name"]
        self._equip_rose_with_best_model(best_algorithm, train_result["trained_strategies"])

        reply = self._build_reply(
            intent=intent,
            message=message,
            question=question,
            train_set=train_set,
            train_result=train_result,
            test_result=test_result,
            best_model_name=best_model_name,
            best_accuracy=best_accuracy,
        )

        logger.info(
            "[SmithCaptainInteractor] chat 완료 | intent=%s algorithm=%s accuracy=%.4f",
            intent,
            best_algorithm,
            best_accuracy,
        )
        return ChatResponse(reply=reply, accuracy=best_accuracy)

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        """스미스 선장의 자기소개 인터렉트"""

        return await self.repository.introduce_myself(
            SmithCaptainQuery(
                id=schema.id,
                name=schema.name,
            )
        )


CrewSmithCaptainInteractor = SmithCaptainInteractor
