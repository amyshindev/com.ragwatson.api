from fastapi import APIRouter

from titanic.adapter.inbound.api.v1.andrew_router import andrew_router
from titanic.adapter.inbound.api.v1.cal_router import cal_router
from titanic.adapter.inbound.api.v1.hartley_router import hartley_router
from titanic.adapter.inbound.api.v1.isidor_router import isidor_router
from titanic.adapter.inbound.api.v1.jack_router import jack_router
from titanic.adapter.inbound.api.v1.james_router import james_router
from titanic.adapter.inbound.api.v1.rose_router import rose_router
from titanic.adapter.inbound.api.v1.ruth_router import ruth_router
from titanic.adapter.inbound.api.v1.smith_router import smith_router
from titanic.adapter.inbound.api.v1.titanic_query_router import titanic_query_router
from titanic.adapter.inbound.api.v1.walter_router import walter_router

titanic_router = APIRouter()
titanic_router.include_router(andrew_router)
titanic_router.include_router(cal_router)
titanic_router.include_router(hartley_router)
titanic_router.include_router(isidor_router)
titanic_router.include_router(jack_router)
titanic_router.include_router(james_router)
titanic_router.include_router(rose_router)
titanic_router.include_router(ruth_router)
titanic_router.include_router(smith_router)
titanic_router.include_router(titanic_query_router)
titanic_router.include_router(walter_router)

__all__ = ["titanic_router"]
