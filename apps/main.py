import asyncio
import logging
from contextlib import asynccontextmanager
from typing import List

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import text

from adapters.db_check_adapter import db_check_adapter
from domain_intake.router import router as domain_intake_router
from core.config import is_database_configured
from database import dispose_engine
from db.session import DbSession
from matrix.app.keymaker import keymaker
from secom.app.controllers.user_controller import UserController
from secom.app.models.schemas import UserResponse
from secom.app.schemas import LoginRequest, LoginResponse, SignupRequest, SignupResponse
def _configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:\t%(message)s",
        force=True,
    )


_configure_logging()
log = logging.getLogger(__name__)

# Same `.env` rule as before: `backend/.env` when `main` lives under `apps/`.
_env_path = Path(__file__).resolve().parent.parent / ".env"
keymaker.bootstrap(env_file=_env_path if _env_path.is_file() else None)


class ChatRequest(BaseModel):
    """채팅 요청 본문. 사용자 메시지를 JSON으로 전달합니다."""

    message: str = Field(..., min_length=1, description="사용자 메시지")


class ChatResponse(BaseModel):
    reply: str


async def _startup_db() -> None:
    if not is_database_configured():
        log.info("DB skipped (DATABASE_URL not set)")
        return
    from secom.app.db_init import init_secom_tables

    await init_secom_tables()
    log.info("DB ready (tables)")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _configure_logging()
    await _startup_db()
    try:
        yield
    finally:
        await dispose_engine()



app = FastAPI(title="Amy Shin Main Page", lifespan=lifespan)

app.include_router(domain_intake_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request, call_next):
    log.info("→ %s %s", request.method, request.url.path)
    response = await call_next(request)
    log.info("← %s %s %s", request.method, request.url.path, response.status_code)
    return response


class TitanicQARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)


class TitanicQAResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]


@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "gemini": keymaker.has_gemini(),
        "database": is_database_configured(),
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    if not keymaker.has_gemini():
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY is not set (use backend/.env or environment).",
        )

    model = keymaker.get_gemini_model()
    if model is None:
        raise HTTPException(status_code=503, detail="Gemini model is not configured.")

    def _generate():
        return model.generate_content(body.message)

    try:
        response = await asyncio.to_thread(_generate)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    try:
        text = response.text
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail="Model returned no text (empty or blocked).",
        )

    return ChatResponse(reply=text)


@app.get("/health/db")
async def health_db(session: DbSession):
    await session.execute(text("SELECT 1"))
    return {"db": "ok"}


@app.get("/db-check")
async def check_db(session: DbSession):
    return await db_check_adapter.check_now(session)


@app.get("/titanic/data")
def read_titanic_data():
    from titanic.app.james_controller import JamesController

    james = JamesController()
    df = james.get_data()

    return df.to_dict(orient="records")


@app.get("/titanic/count")
def read_titanic_count():
    from titanic.app.james_controller import JamesController

    james = JamesController()
    count = james.get_count()

    return {"count": count}


@app.get("/titanic/tree")
def read_titanic_tree():
    from titanic.app.james_controller import JamesController

    james = JamesController()
    tree = james.has_decision_tree_model()

    return {"tree": tree}


@app.get("/titanic/model")
def read_titanic_model():
    from titanic.app.james_controller import JamesController

    controller = JamesController()
    model_name = controller.get_model_name_and_accuracy()
    return JSONResponse(content=jsonable_encoder(model_name))


@app.get("/doro/data")
def read_doro_data():
    from doro.app.doro_director import DoroDirector

    doro_director = DoroDirector()
    df = doro_director.get_data()

    return df.to_dict(orient="records")


@app.post("/signup", response_model=SignupResponse)
async def signup(req: SignupRequest, session: DbSession) -> SignupResponse:
    log.info("POST /signup 요청 수신 email=%s", req.email)
    if not is_database_configured():
        raise HTTPException(status_code=503, detail="DATABASE_URL is not set.")
    try:
        await UserController(session).save_user(req)
        await session.commit()
        return SignupResponse(
            user=UserResponse(
                id=req.userId,
                email=str(req.email),
                username=req.username,
                nickname=req.nickname,
                role=req.role,
            )
        )
    except HTTPException:
        await session.rollback()
        raise
    except Exception as exc:
        await session.rollback()
        log.exception("signup failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, session: DbSession) -> LoginResponse:
    log.info("POST /login 요청 수신 email=%s", req.email)
    if not is_database_configured():
        raise HTTPException(status_code=503, detail="DATABASE_URL is not set.")
    try:
        user = await UserController(session).login(req)
        await session.commit()
        return LoginResponse(user=user)
    except HTTPException:
        await session.rollback()
        raise
    except Exception as exc:
        await session.rollback()
        log.exception("login failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )
