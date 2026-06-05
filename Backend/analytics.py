"""
Analytics router — all /api/* endpoints.

POST /api/analyze   — full pipeline (intent → analysis → LLM)
POST /api/chat      — alias for /api/analyze (conversational UX)
GET  /api/kpis      — top-level KPI cards
GET  /api/categories
GET  /api/regions
GET  /api/channels
GET  /api/campaigns
"""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.models.schemas import (
    AnalyticsResponse,
    ErrorResponse,
    KPIsResponse,
    KPIItem,
    ListResponse,
    QueryRequest,
)
from app.services.data_service import get_dataframe
from app.services.analysis_service import run_analytics_pipeline
from app.services.llm_service import get_llm_explanation

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Analytics"])


# ── helpers ───────────────────────────────────────────────────────────────────

def _get_df():
    try:
        return get_dataframe()
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )


# ── /api/analyze ──────────────────────────────────────────────────────────────

@router.post(
    "/analyze",
    response_model=AnalyticsResponse,
    responses={422: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
    summary="Run the full analytics pipeline for a natural-language query",
    description=(
        "Detects intent, computes Pandas statistics, validates results, "
        "scores confidence, generates a base insight, then enriches it "
        "with an LLM explanation via Groq."
    ),
)
async def analyze(body: QueryRequest) -> AnalyticsResponse:
    settings = get_settings()
    df = _get_df()

    # 1-6: deterministic pipeline (sync, fast)
    pipeline_result = run_analytics_pipeline(body.query, df)

    # 7: LLM enrichment (async, may be slow)
    validation = pipeline_result["validation"]
    if not validation.get("blocked", False):
        llm_explanation = await get_llm_explanation(
            result={
                "intent": pipeline_result["intent"],
                "raw_stats": {},          # re-built inside llm_layer via summary
                "table": None,
            },
            base_insight=pipeline_result["base_insight"],
            confidence=pipeline_result["confidence"],
            api_key=settings.groq_api_key,
        )
    else:
        llm_explanation = validation.get("block_reason", pipeline_result["base_insight"])

    pipeline_result["llm_explanation"] = llm_explanation

    return AnalyticsResponse(**pipeline_result)


# ── /api/chat (alias) ─────────────────────────────────────────────────────────

@router.post(
    "/chat",
    response_model=AnalyticsResponse,
    responses={422: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
    summary="Conversational alias for /api/analyze",
    description="Identical to /api/analyze; provided for conversational-UI clients.",
)
async def chat(body: QueryRequest) -> AnalyticsResponse:
    return await analyze(body)


# ── /api/kpis ─────────────────────────────────────────────────────────────────

@router.get(
    "/kpis",
    response_model=KPIsResponse,
    summary="Return top-level KPI cards from the dataset",
)
def get_kpis() -> KPIsResponse:
    df = _get_df()

    avg_sales   = round(df["monthly_sales"].mean(), 2)
    total_sales = round(df["monthly_sales"].sum(), 2)
    avg_roi     = round(df["ROI"].mean(), 4)
    avg_spend   = round(df["marketing_spend"].mean(), 2)
    top_cat     = df.groupby("Category")["monthly_sales"].mean().idxmax()
    top_channel = df.groupby("Marketing_Channel")["ROI"].mean().idxmax()

    return KPIsResponse(
        kpis=[
            KPIItem(label="Avg Monthly Sales",   value=avg_sales,   unit="$"),
            KPIItem(label="Total Sales",          value=total_sales, unit="$"),
            KPIItem(label="Avg ROI",              value=avg_roi,     unit=""),
            KPIItem(label="Avg Marketing Spend",  value=avg_spend,   unit="$"),
            KPIItem(label="Top Sales Category",   value=top_cat,     unit=""),
            KPIItem(label="Best ROI Channel",     value=top_channel, unit=""),
        ]
    )


# ── /api/categories ───────────────────────────────────────────────────────────

@router.get(
    "/categories",
    response_model=ListResponse,
    summary="List all unique product/business categories in the dataset",
)
def get_categories() -> ListResponse:
    df = _get_df()
    return ListResponse(items=sorted(df["Category"].dropna().unique().tolist()))


# ── /api/regions ──────────────────────────────────────────────────────────────

@router.get(
    "/regions",
    response_model=ListResponse,
    summary="List all unique geographic regions in the dataset",
)
def get_regions() -> ListResponse:
    df = _get_df()
    return ListResponse(items=sorted(df["Region"].dropna().unique().tolist()))


# ── /api/channels ─────────────────────────────────────────────────────────────

@router.get(
    "/channels",
    response_model=ListResponse,
    summary="List all unique marketing channels in the dataset",
)
def get_channels() -> ListResponse:
    df = _get_df()
    return ListResponse(items=sorted(df["Marketing_Channel"].dropna().unique().tolist()))


# ── /api/campaigns ────────────────────────────────────────────────────────────

@router.get(
    "/campaigns",
    response_model=ListResponse,
    summary="List all unique campaign types in the dataset",
)
def get_campaigns() -> ListResponse:
    df = _get_df()
    return ListResponse(items=sorted(df["Campaign_Type"].dropna().unique().tolist()))
