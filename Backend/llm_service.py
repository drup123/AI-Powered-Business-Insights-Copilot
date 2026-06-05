"""
LLM service — thin async wrapper around the existing synchronous llm_layer.
Runs Groq calls in a thread pool to avoid blocking the event loop.
"""
from __future__ import annotations

import asyncio
import logging
from functools import partial

# ── existing business-logic modules (unchanged) ──────────────────────────────
from app.llm_layer import build_structured_summary, generate_insight

logger = logging.getLogger(__name__)


async def get_llm_explanation(
    result: dict,
    base_insight: str,
    confidence: dict,
    api_key: str,
) -> str:
    """
    Build the structured summary, then ask Groq to explain it.
    Returns the explanation string (or a fallback message on error).
    """
    if not api_key:
        logger.warning("No Groq API key configured; skipping LLM call.")
        return "⚠️ LLM explanation unavailable — GROQ_API_KEY not set."

    structured_summary = build_structured_summary(result, base_insight, confidence)

    loop = asyncio.get_event_loop()
    try:
        insight_dict = await loop.run_in_executor(
            None,
            partial(generate_insight, structured_summary, api_key),
        )
        return insight_dict.get("explanation", base_insight)
    except Exception as exc:
        logger.exception("LLM call failed: %s", exc)
        return f"LLM unavailable: {exc}"
