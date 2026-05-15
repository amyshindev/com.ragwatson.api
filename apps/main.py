import asyncio
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
from core.config import is_database_configured
from db.session import DbSession, dispose_engine
from matrix.app.keymaker import keymaker

# Same `.env` rule as before: `backend/.env` when `main` lives under `apps/`.
_env_path = Path(__file__).resolve().parent.parent / ".env"
keymaker.bootstrap(env_file=_env_path if _env_path.is_file() else None)


class ChatRequest(BaseModel):
    """채팅 요청 본문. 사용자 메시지를 JSON으로 전달합니다."""

    message: str = Field(..., min_length=1, description="사용자 메시지")


class ChatResponse(BaseModel):
    reply: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await dispose_engine()


# ------------------------------------------------------------------------------------------------

app = FastAPI(title="Amy Shin Main Page", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
