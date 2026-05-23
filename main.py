"""
main.py — FastAPI application entry point.

This file is intentionally minimal. All logic lives in:
  - config.py         → settings
  - database/         → ChromaDB management
  - agents/           → RAG pipeline
  - api/              → routes & schemas
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CORS_ORIGINS
from database import initialize_database
from api.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting AI Personal Trainer Backend …")
    try:
        initialize_database()
        logger.info("✅ ChromaDB ready.")
    except Exception as exc:
        logger.error("❌ ChromaDB init failed: %s", exc)
    yield
    logger.info("🛑 Shutting down.")


app = FastAPI(
    title="AI Personal Trainer Agent",
    description="AI gym assistant: workout plans, nutrition, schedules, exercise guides.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
