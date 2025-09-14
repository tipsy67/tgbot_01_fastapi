import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from api_app.core.config import settings
from api_app.core.db_helper import db_helper
from api_app.core.taskiq_broker import broker, redis_source
from api_app.routers import router


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    if not broker.is_worker_process:
        await broker.startup()
    await redis_source.startup()

    yield
    # shutdown
    await db_helper.dispose()

    if not broker.is_worker_process:
        await broker.shutdown()
    await redis_source.shutdown()


api_main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    settings.webapp.url,
]

# Настройка CORS
api_main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


@api_main_app.get("/")
async def root():
    return {"message": "Hello!"}


api_main_app.include_router(router)
