from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field


# ── Requests ─────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        max_length=500,
        examples=["Which marketing channel gives highest ROI?"],
        description="Natural-language business question about the dataset",
    )


# ── Nested response pieces ────────────────────────────────────────────────────

class ConfidenceSchema(BaseModel):
    level: str = Field(description="High | Medium | Low")
    score: float = Field(ge=0.0, le=1.0)
    reason: str


class ValidationSchema(BaseModel):
    flags: list[str] = Field(default_factory=list)
    blocked: bool = False
    block_reason: str = ""


class ChartData(BaseModel):
    chart_type: str = Field(description="bar | scatter | line")
    title: str = ""
    x_label: str = ""
    y_label: str = ""
    x: list[Any] = Field(default_factory=list)
    y: list[Any] = Field(default_factory=list)
    color: list[str] | None = None   # optional per-point color grouping label
    extra: dict[str, Any] = Field(default_factory=dict)   # hover data, etc.


class ChartsSchema(BaseModel):
    primary: ChartData
    secondary: ChartData


# ── Main response ─────────────────────────────────────────────────────────────

class AnalyticsResponse(BaseModel):
    success: bool = True
    query: str
    intent: str
    confidence: ConfidenceSchema
    validation: ValidationSchema
    base_insight: str
    llm_explanation: str
    table_data: list[dict[str, Any]] = Field(default_factory=list)
    charts: ChartsSchema


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    detail: str | None = None


# ── Utility / lookup responses ────────────────────────────────────────────────

class KPIItem(BaseModel):
    label: str
    value: float | str
    unit: str = ""
    trend: str | None = None   # up | down | flat


class KPIsResponse(BaseModel):
    success: bool = True
    kpis: list[KPIItem]


class ListResponse(BaseModel):
    success: bool = True
    items: list[str]


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
    dataset_loaded: bool
    row_count: int
