__author__ = "Sam"

from contextlib import asynccontextmanager

from arq import create_pool
from arq.connections import RedisSettings
from fastapi import FastAPI

from api.routes import router
from core.config import settings


def _redis_settings() -> RedisSettings:
    return RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        database=settings.redis_db,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # single shared pool for the lifetime of the process
    app.state.arq_pool = await create_pool(_redis_settings())
    yield
    await app.state.arq_pool.close()


app = FastAPI(
    title="scraper-service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")
