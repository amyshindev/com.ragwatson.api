from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from db.session import DbSession
from titanic.app.use_cases.titanic_query_impl import TitanicQueryUseCase

router = APIRouter(prefix="/titanic", tags=["titanic-query"])
_use_case = TitanicQueryUseCase()


@router.get("/data")
async def read_titanic_data(session: DbSession):
    return await _use_case.get_passenger_data(session)


@router.get("/count")
async def read_titanic_count(session: DbSession):
    count = await _use_case.get_passenger_count(session)
    return {"count": count}


@router.get("/tree")
def read_titanic_tree():
    return {"tree": _use_case.has_decision_tree_model()}


@router.get("/model")
def read_titanic_model():
    model_name = _use_case.get_model_name()
    return JSONResponse(content=jsonable_encoder(model_name))
