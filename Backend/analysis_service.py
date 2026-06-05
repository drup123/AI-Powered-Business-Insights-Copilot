"""
Analysis service — thin orchestration layer that calls the existing
business-logic modules without any modification.

Pipeline:
  query → detect_intent → process_query → validate_result
        → compute_confidence → generate_base_insight
"""
from __future__ import annotations

import logging
from typing import Any

import pandas as pd

# ── existing business-logic modules (unchanged) ──────────────────────────────
from app.intent_engine import detect_intent
from app.analysis_engine import (
    process_query,
    validate_result,
    compute_confidence,
    generate_base_insight,
)
from app.models.schemas import (
    AnalyticsResponse,
    ConfidenceSchema,
    ValidationSchema,
    ChartData,
    ChartsSchema,
)

logger = logging.getLogger(__name__)


# ── chart serialisation helpers ───────────────────────────────────────────────

def _bar_chart(tbl: pd.DataFrame, x_col: str, y_col: str, title: str) -> ChartData:
    return ChartData(
        chart_type="bar",
        title=title,
        x_label=x_col,
        y_label=y_col,
        x=tbl[x_col].tolist(),
        y=tbl[y_col].tolist(),
    )


def _scatter_chart(df: pd.DataFrame, color_col: str) -> ChartData:
    """Global scatter: marketing_spend vs monthly_sales coloured by group."""
    return ChartData(
        chart_type="scatter",
        title="Marketing Spend vs Monthly Sales",
        x_label="marketing_spend",
        y_label="monthly_sales",
        x=df["marketing_spend"].tolist(),
        y=df["monthly_sales"].tolist(),
        color=df[color_col].tolist(),
        extra={"roi": df["ROI"].tolist()},
    )


def _build_charts(df: pd.DataFrame, result: dict) -> ChartsSchema:
    intent = result["intent"]
    tbl = result["table"]

    empty = ChartData(chart_type="bar", title="No data available")

    # Primary chart
    if tbl is None or (isinstance(tbl, pd.DataFrame) and tbl.empty):
        primary = empty
    elif intent == "SALES_TREND":
        primary = _bar_chart(tbl, "Category", "Avg Monthly Sales",
                             "Avg Monthly Sales by Category")
    elif intent == "MARKETING_IMPACT":
        primary = _bar_chart(tbl, "Category", "Avg Marketing Spend",
                             "Avg Marketing Spend by Category")
    elif intent == "ROI_ANALYSIS":
        primary = _bar_chart(tbl, "Category", "Avg ROI",
                             "Avg ROI by Category")
    elif intent == "REGION_ANALYSIS":
        primary = _bar_chart(tbl, "Region", "Avg Monthly Sales",
                             "Avg Monthly Sales by Region")
    elif intent == "CHANNEL_ANALYSIS":
        primary = _bar_chart(tbl, "Marketing_Channel", "Avg ROI",
                             "Avg ROI by Marketing Channel")
    elif intent == "CAMPAIGN_ANALYSIS":
        primary = _bar_chart(tbl, "Campaign_Type", "Avg ROI",
                             "Avg ROI by Campaign Type")
    else:  # GENERAL_INSIGHTS
        primary = _bar_chart(tbl, "Category", "Avg_Sales",
                             "Overview — Avg Monthly Sales by Category")

    # Secondary chart — always spend vs sales scatter
    color_col = "Region" if intent == "REGION_ANALYSIS" else "Category"
    secondary = _scatter_chart(df, color_col)

    return ChartsSchema(primary=primary, secondary=secondary)


# ── main pipeline ─────────────────────────────────────────────────────────────

def run_analytics_pipeline(query: str, df: pd.DataFrame) -> dict[str, Any]:
    """
    Execute the full analytics pipeline and return a plain dict
    ready to be validated into AnalyticsResponse.
    """
    # 1. Intent detection
    intent = detect_intent(query)

    # 2. Out-of-scope fast-return
    if intent == "OUT_OF_SCOPE":
        return _out_of_scope_response(query)

    # 3. Pandas computation
    result = process_query(df, intent)

    # 4. Guardrails / validation
    validation = validate_result(result)

    # 5. Confidence scoring
    confidence = compute_confidence(result)

    # 6. Base (deterministic) insight
    base_insight = generate_base_insight(result, confidence)

    # 7. Table → JSON
    tbl = result.get("table")
    table_data: list[dict] = []
    if tbl is not None and isinstance(tbl, pd.DataFrame) and not tbl.empty:
        table_data = tbl.to_dict(orient="records")

    # 8. Charts (serialised — no Plotly objects)
    charts = _build_charts(df, result)

    return {
        "query": query,
        "intent": intent,
        "confidence": confidence,
        "validation": validation,
        "base_insight": base_insight,
        "llm_explanation": "",          # filled by llm_service
        "table_data": table_data,
        "charts": charts,
    }


def _out_of_scope_response(query: str) -> dict[str, Any]:
    return {
        "query": query,
        "intent": "OUT_OF_SCOPE",
        "confidence": {"level": "Low", "score": 0.0,
                       "reason": "Query is outside the dataset scope"},
        "validation": {"flags": ["This topic is not covered by the current dataset."],
                       "blocked": True,
                       "block_reason": "Out-of-scope query"},
        "base_insight": "This question cannot be answered from the available dataset.",
        "llm_explanation": "",
        "table_data": [],
        "charts": ChartsSchema(
            primary=ChartData(chart_type="bar", title="No data"),
            secondary=ChartData(chart_type="scatter", title="No data"),
        ),
    }
