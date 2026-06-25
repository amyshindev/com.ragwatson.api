from fastapi import APIRouter

from siliconvalley.adapter.inbound.api.v1.bighetti_hr_router import bighetti_hr_router
from siliconvalley.adapter.inbound.api.v1.dinesh_dash_router import dinesh_dash_router
from siliconvalley.adapter.inbound.api.v1.dunn_coo_router import dunn_coo_router
from siliconvalley.adapter.inbound.api.v1.gilfoyle_system_router import gilfoyle_system_router
from siliconvalley.adapter.inbound.api.v1.hendricks_ceo_router import hendricks_ceo_router

siliconvalley_router = APIRouter()
siliconvalley_router.include_router(hendricks_ceo_router)
siliconvalley_router.include_router(gilfoyle_system_router)
siliconvalley_router.include_router(dinesh_dash_router)
siliconvalley_router.include_router(dunn_coo_router)
siliconvalley_router.include_router(bighetti_hr_router)

__all__ = ["siliconvalley_router"]
