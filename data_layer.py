import os
import pandas as pd
import streamlit as st
from config import DATASET_PATH

@st.cache_data(show_spinner=False)
def load_data(path: str = DATASET_PATH) -> pd.DataFrame | None:
    """Load and validate the CSV dataset."""
    if not os.path.exists(path):
        st.stop()
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    required = {"Category", "monthly_sales", "marketing_spend", "ROI",
    "Region", "Marketing_Channel", "Campaign_Type"}
    if not required.issubset(df.columns):
        st.error(f"Dataset must contain: {required}  —  found: {list(df.columns)}")
        st.stop()
    for col in ["monthly_sales", "marketing_spend", "ROI"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.dropna(subset=["monthly_sales", "marketing_spend", "ROI"], inplace=True)
    return df

