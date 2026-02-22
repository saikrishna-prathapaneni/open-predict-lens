"""SurrealDB connection and lifecycle."""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from surrealdb import AsyncSurreal

from app.config import settings

# Module-level client for app lifespan; set in lifespan, read in routes
_db: AsyncSurreal | None = None


def get_db() -> AsyncSurreal:
    """Return the shared SurrealDB client. Use after app startup."""
    if _db is None:
        raise RuntimeError("SurrealDB not connected; app may not be started yet")
    return _db


async def connect_surreal() -> AsyncSurreal:
    """Create connection, sign in as root, and select namespace/database."""
    # Use ws:// for stateful connection (session/token preserved)
    url = settings.surreal_url.replace("http://", "ws://", 1).replace("https://", "wss://", 1)
    db = AsyncSurreal(url)
    await db.signin(
        {
            "username": settings.surreal_user,
            "password": settings.surreal_pass,
        }
    )
    await db.use(namespace=settings.surreal_ns, database=settings.surreal_db)
    return db


async def close_surreal() -> None:
    """Close the shared SurrealDB connection."""
    global _db
    if _db is not None:
        await _db.close()
        _db = None


@asynccontextmanager
async def surreal_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context: set global client on startup, clear on shutdown."""
    global _db
    _db = await connect_surreal()
    try:
        yield
    finally:
        await close_surreal()
