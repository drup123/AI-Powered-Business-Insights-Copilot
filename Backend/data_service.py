"""
Data service — owns the single DataFrame instance for the process lifetime.
Loaded once during FastAPI lifespan; every request reads the cached copy.
"""
from __future__ import annotations

import os
import logging

import pandas as pd

logger = logging.getLogger(__name__)

# Module-level singleton; populated by `load_dataset()` at startup.
_df: pd.DataFrame | None = None

REQUIRED_COLUMNS = {
    "Category", "monthly_sales", "marketing_spend",
    "ROI", "Region", "Marketing_Channel", "Campaign_Type",
}


def load_dataset(path: str) -> pd.DataFrame:
    """
    Read, validate, and cache the CSV.
    Raises RuntimeError on any problem so FastAPI lifespan can surface it clearly.
    """
    global _df

    if not os.path.exists(path):
        raise RuntimeError(f"Dataset not found at: {path}")

    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise RuntimeError(
            f"Dataset is missing required columns: {missing}. "
            f"Found: {list(df.columns)}"
        )

    for col in ("monthly_sales", "marketing_spend", "ROI"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    before = len(df)
    df.dropna(subset=["monthly_sales", "marketing_spend", "ROI"], inplace=True)
    dropped = before - len(df)
    if dropped:
        logger.warning("Dropped %d rows with null numeric values.", dropped)

    _df = df
    logger.info("Dataset loaded: %d rows, %d columns from '%s'", len(df), len(df.columns), path)
    return df


def get_dataframe() -> pd.DataFrame:
    """Return the cached DataFrame. Raises if not yet loaded."""
    if _df is None:
        raise RuntimeError("Dataset has not been loaded. Check startup logs.")
    return _df
