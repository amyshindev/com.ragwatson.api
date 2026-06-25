from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinResponse
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.dependencies.crew_hartley_violin_provider import (
    get_hartley_violin_correlation_use_case,
    get_hartley_violin_use_case,
)

"""
월리스 하틀리 (Wallace Hartley)
타이타닉 밴드의 리더로, 침몰 직전까지 바이올린을 연주하며 승객들을 위로했습니다. 관측·로그·이벤트 흐름을 기록하는 역할에 적합합니다.

추천 파일명: hartley_violin_router.py (Violin: 타이타닉 밴드 리더)
"""
hartley_violin_router = APIRouter(prefix="/titanic/hartley", tags=["hartley"])


@hartley_violin_router.get("/myself")
async def introduce_myself(
    hartley: HartleyViolinUseCase = Depends(get_hartley_violin_use_case),
) -> HartleyViolinResponse:
    return await hartley.introduce_myself(
        HartleyViolinSchema(id=3, name="월리스 하틀리 (Wallace Hartley)")
    )


@hartley_violin_router.get("/correlation")
def get_titanic_correlation(
    hartley: HartleyViolinUseCase = Depends(get_hartley_violin_correlation_use_case),
):
    return hartley.get_correlation_heatmap_response()


# --- 기존: DB 세션 주입 경로 (Neon 인증 필요) ---
# @hartley_violin_router.get("/correlation")
# def get_titanic_correlation(
#     hartley: HartleyViolinUseCase = Depends(get_hartley_violin_use_case),
# ):
#     return hartley.get_correlation_heatmap_response()
