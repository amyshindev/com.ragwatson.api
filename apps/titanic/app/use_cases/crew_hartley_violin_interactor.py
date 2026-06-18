from __future__ import annotations

import io
import logging

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fastapi.responses import StreamingResponse

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.output.crew_hartley_violin_port import HartleyViolinPort
from titanic.app.use_cases.crew_walter_roaster_reader import WalterReader

logger = logging.getLogger(__name__)


class HartleyViolinInteractor(HartleyViolinUseCase):

    def __init__(self, repository: HartleyViolinPort | None = None):
        self.repository = repository

    def _load_titanic_frame(self) -> pd.DataFrame:
        dataset = WalterReader().get_dataset()
        if dataset.empty:
            raise RuntimeError("타이타닉 데이터셋을 불러올 수 없습니다.")
        return dataset

    def _prepare_numeric_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        frame = df.copy()
        if "Sex" in frame.columns:
            frame["Sex"] = (
                frame["Sex"]
                .astype(str)
                .str.lower()
                .map({"male": 0, "female": 1})
                .fillna(0)
            )
        numeric = frame.select_dtypes(include=["number"])
        if numeric.empty:
            raise RuntimeError("상관계수를 계산할 수치형 컬럼이 없습니다.")
        return numeric

    def build_correlation_matrix(self) -> pd.DataFrame:
        '''Pandas로 수치형 피처 간 피어슨 상관계수 행렬을 계산한다.'''
        numeric = self._prepare_numeric_frame(self._load_titanic_frame())
        correlation = numeric.corr()
        logger.info(
            "[HartleyViolinInteractor] correlation matrix | columns=%s",
            list(correlation.columns),
        )
        return correlation

    def build_correlation_heatmap_buffer(self) -> io.BytesIO:
        '''Seaborn/Matplotlib 히트맵을 메모리(BytesIO)에 PNG로 저장한다.'''
        correlation = self.build_correlation_matrix()

        figure, _ = plt.subplots(figsize=(8, 6))
        try:
            sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
            plt.title("Titanic Feature Correlation")

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", bbox_inches="tight")
            buffer.seek(0)
            logger.info("[HartleyViolinInteractor] correlation heatmap generated")
            return buffer
        finally:
            plt.close(figure)

    def get_correlation_heatmap_response(self) -> StreamingResponse:
        '''BytesIO 버퍼를 FastAPI StreamingResponse(image/png)로 반환한다.'''
        buffer = self.build_correlation_heatmap_buffer()
        return StreamingResponse(buffer, media_type="image/png")

    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        '''하틀리 바이올린의 자기소개 인터랙트'''
        if self.repository is None:
            raise RuntimeError("introduce_myself는 DB 레포지토리가 필요합니다.")

        return await self.repository.introduce_myself(HartleyViolinQuery(
            id=schema.id,
            name=schema.name,
        ))


CrewHartleyViolinInteractor = HartleyViolinInteractor
