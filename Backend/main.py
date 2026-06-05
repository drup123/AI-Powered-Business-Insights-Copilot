"""
main.py — FastAPI application entry point.

• Dataset loaded ONCE during lifespan startup.
• CORS configured for React dev servers (localhost:3000 + localhost:5173).
• Swagger UI available at /docs, ReDoc at /redoc.
"""
from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.models.schemas import HealthResponse, ErrorResponse
from app.routes.analytics import router as analytics_router
from app.services.data_service import load_dataset, get_dataframe

# ── logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


# ── lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load dataset once at startup; nothing to tear down."""
    settings = get_settings()
    dataset_path = settings.dataset_path

    # Allow an absolute path override via environment
    if not os.path.isabs(dataset_path):
        # Resolve relative to the repo root (parent of app/)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_path = os.path.join(base_dir, dataset_path)

    logger.info("Loading dataset from: %s", dataset_path)
    try:
        load_dataset(dataset_path)
        logger.info("Dataset ready.")
    except RuntimeError as exc:
        logger.critical("STARTUP FAILED — could not load dataset: %s", exc)
        raise

    yield   # application runs here


# ── app factory ───────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Production-ready REST API for AI-Powered Business Insights Copilot. "
            "Exposes natural-language analytics over a business CSV dataset, "
            "enriched with Groq LLM explanations."
        ),
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── global exception handler ──────────────────────────────────────────────
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal server error",
                     "detail": str(exc)},
        )

    # ── routers ───────────────────────────────────────────────────────────────
    app.include_router(analytics_router)

    # ── root & health ─────────────────────────────────────────────────────────
    @app.get(
        "/",
        tags=["System"],
        summary="API root — returns basic metadata",
    )
    def root():
        s = get_settings()
        return {"name": s.app_name, "version": s.app_version,
                "docs": "/docs", "health": "/health"}

    @app.get(
        "/health",
        response_model=HealthResponse,
        tags=["System"],
        summary="Health-check endpoint",
    )
    def health():
        try:
            df = get_dataframe()
            return HealthResponse(
                status="ok",
                version=get_settings().app_version,
                dataset_loaded=True,
                row_count=len(df),
            )
        except RuntimeError:
            return JSONResponse(
                status_code=503,
                content={"status": "degraded", "version": get_settings().app_version,
                         "dataset_loaded": False, "row_count": 0},
            )

    return app


app = create_app()
