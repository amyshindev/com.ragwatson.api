"""Interactor 공통 commit/rollback (TASK_ML_DB_SETUP §8)."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)

T = TypeVar("T")


async def run_committed(session: AsyncSession, work: Callable[[], Awaitable[T]]) -> T:
    try:
        result = await work()
        await session.commit()
        return result
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=409, detail="Duplicate or invalid FK"
        ) from exc
    except OperationalError as exc:
        await session.rollback()
        raise HTTPException(status_code=503, detail="DB unavailable") from exc
    except HTTPException:
        await session.rollback()
        raise
    except Exception as exc:
        await session.rollback()
        log.exception("ml_data transaction failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
