import pandas as pd
from config import CORR_STRONG, CORR_MODERATE, CORR_WEAK, DIFF_THRESHOLD

def process_query(df: pd.DataFrame, intent: str) -> dict:
    """
    Pure Pandas computation layer.
    Returns a result dict containing: intent, table, raw_stats.
    """
    result = {"intent": intent, "table": None, "raw_stats": {}}

    if intent == "SALES_TREND":
        tbl = (
            df.groupby("Category", as_index=False)["monthly_sales"]
            .mean()
            .sort_values("monthly_sales", ascending=False)
            .rename(columns={"monthly_sales": "Avg Monthly Sales"})
        )
        tbl["Avg Monthly Sales"] = tbl["Avg Monthly Sales"].round(2)
        top_val  = tbl.iloc[0]["Avg Monthly Sales"]
        low_val  = tbl.iloc[-1]["Avg Monthly Sales"]
        result["table"] = tbl
        result["raw_stats"] = {
            "top_category":    tbl.iloc[0]["Category"],
            "top_value":       top_val,
            "lowest_category": tbl.iloc[-1]["Category"],
            "lowest_value":    low_val,
            "difference":      round(top_val - low_val, 2),
            "relative_diff":   round(abs(top_val - low_val) / max(top_val, 1), 4),
            "num_categories":  len(tbl),
            "all_values":      tbl.set_index("Category")["Avg Monthly Sales"].to_dict(),
            "metric":          "Avg Monthly Sales",
        }

    elif intent == "MARKETING_IMPACT":
        corr_val = round(df["marketing_spend"].corr(df["monthly_sales"]), 4)
        slope    = round(
            df["monthly_sales"].cov(df["marketing_spend"]) / df["marketing_spend"].var(), 4
        )
        tbl = (
            df.groupby("Category", as_index=False)[["marketing_spend", "monthly_sales"]]
            .mean()
            .round(2)
            .rename(columns={
                "marketing_spend": "Avg Marketing Spend",
                "monthly_sales":   "Avg Monthly Sales",
            })
        )
        result["table"] = tbl
        result["raw_stats"] = {
            "correlation": corr_val,
            "slope":       slope,
            "metric":      "Marketing Spend vs Monthly Sales",
        }

    elif intent == "ROI_ANALYSIS":
        tbl = (
            df.groupby("Category", as_index=False)["ROI"]
            .mean()
            .sort_values("ROI", ascending=False)
            .rename(columns={"ROI": "Avg ROI"})
        )
        tbl["Avg ROI"] = tbl["Avg ROI"].round(4)
        top_val  = tbl.iloc[0]["Avg ROI"]
        low_val  = tbl.iloc[-1]["Avg ROI"]
        result["table"] = tbl
        result["raw_stats"] = {
            "top_category":    tbl.iloc[0]["Category"],
            "top_value":       top_val,
            "lowest_category": tbl.iloc[-1]["Category"],
            "lowest_value":    low_val,
            "difference":      round(top_val - low_val, 4),
            "relative_diff":   round(abs(top_val - low_val) / max(top_val, 1), 4),
            "num_categories":  len(tbl),
            "all_values":      tbl.set_index("Category")["Avg ROI"].to_dict(),
            "metric":          "Avg ROI",
        }

    elif intent == "REGION_ANALYSIS":
        tbl = (
            df.groupby("Region", as_index=False)["monthly_sales"]
            .mean()
            .sort_values("monthly_sales", ascending=False)
            .rename(columns={"monthly_sales": "Avg Monthly Sales"})
        )
        tbl["Avg Monthly Sales"] = tbl["Avg Monthly Sales"].round(2)
        top_val = tbl.iloc[0]["Avg Monthly Sales"]
        low_val = tbl.iloc[-1]["Avg Monthly Sales"]
        result["table"] = tbl
        result["raw_stats"] = {
            "top_category":    tbl.iloc[0]["Region"],
            "top_value":       top_val,
            "lowest_category": tbl.iloc[-1]["Region"],
            "lowest_value":    low_val,
            "difference":      round(top_val - low_val, 2),
            "relative_diff":   round(abs(top_val - low_val) / max(top_val, 1), 4),
            "num_categories":  len(tbl),
            "all_values":      tbl.set_index("Region")["Avg Monthly Sales"].to_dict(),
            "group_by":        "Region",
            "metric":          "Avg Monthly Sales",
        }

    elif intent == "CHANNEL_ANALYSIS":
        tbl = (
            df.groupby("Marketing_Channel", as_index=False)["ROI"]
            .mean()
            .sort_values("ROI", ascending=False)
            .rename(columns={"ROI": "Avg ROI"})
        )
        tbl["Avg ROI"] = tbl["Avg ROI"].round(4)
        top_val = tbl.iloc[0]["Avg ROI"]
        low_val = tbl.iloc[-1]["Avg ROI"]
        result["table"] = tbl
        result["raw_stats"] = {
            "top_category":    tbl.iloc[0]["Marketing_Channel"],
            "top_value":       top_val,
            "lowest_category": tbl.iloc[-1]["Marketing_Channel"],
            "lowest_value":    low_val,
            "difference":      round(top_val - low_val, 4),
            "relative_diff":   round(abs(top_val - low_val) / max(top_val, 1), 4),
            "num_categories":  len(tbl),
            "all_values":      tbl.set_index("Marketing_Channel")["Avg ROI"].to_dict(),
            "group_by":        "Marketing_Channel",
            "metric":          "Avg ROI",
        }

    elif intent == "CAMPAIGN_ANALYSIS":
        tbl = (
            df.groupby("Campaign_Type", as_index=False)["ROI"]
            .mean()
            .sort_values("ROI", ascending=False)
            .rename(columns={"ROI": "Avg ROI"})
        )
        tbl["Avg ROI"] = tbl["Avg ROI"].round(4)
        top_val = tbl.iloc[0]["Avg ROI"]
        low_val = tbl.iloc[-1]["Avg ROI"]
        result["table"] = tbl
        result["raw_stats"] = {
            "top_category":    tbl.iloc[0]["Campaign_Type"],
            "top_value":       top_val,
            "lowest_category": tbl.iloc[-1]["Campaign_Type"],
            "lowest_value":    low_val,
            "difference":      round(top_val - low_val, 4),
            "relative_diff":   round(abs(top_val - low_val) / max(top_val, 1), 4),
            "num_categories":  len(tbl),
            "all_values":      tbl.set_index("Campaign_Type")["Avg ROI"].to_dict(),
            "group_by":        "Campaign_Type",
            "metric":          "Avg ROI",
        }

    elif intent == "TIME_TREND":
        result["table"] = pd.DataFrame()
        result["raw_stats"] = {}

    else:  # GENERAL_INSIGHTS
        corr_val = round(df["marketing_spend"].corr(df["monthly_sales"]), 4)
        sales_by_cat = df.groupby("Category")["monthly_sales"].mean()
        roi_by_cat   = df.groupby("Category")["ROI"].mean()
        tbl = (
            df.groupby("Category", as_index=False)
            .agg(
                Avg_Sales=("monthly_sales",   "mean"),
                Avg_Spend=("marketing_spend", "mean"),
                Avg_ROI  =("ROI",             "mean"),
            )
            .round(2)
            .sort_values("Avg_Sales", ascending=False)
        )
        top_sales_cat  = sales_by_cat.idxmax()
        top_sales_val  = round(sales_by_cat.max(), 2)
        low_sales_cat  = sales_by_cat.idxmin()
        low_sales_val  = round(sales_by_cat.min(), 2)
        result["table"] = tbl
        result["raw_stats"] = {
            "top_category":    top_sales_cat,
            "top_value":       top_sales_val,
            "lowest_category": low_sales_cat,
            "lowest_value":    low_sales_val,
            "difference":      round(top_sales_val - low_sales_val, 2),
            "relative_diff":   round(abs(top_sales_val - low_sales_val) / max(top_sales_val, 1), 4),
            "best_roi_cat":    roi_by_cat.idxmax(),
            "best_roi_val":    round(roi_by_cat.max(), 4),
            "correlation":     corr_val,
            "avg_sales":       round(df["monthly_sales"].mean(), 2),
            "avg_spend":       round(df["marketing_spend"].mean(), 2),
            "num_categories":  len(tbl),
            "metric":          "Avg Monthly Sales",
        }

    return result


def validate_result(result: dict) -> dict:
    """
    Python-level guardrails applied BEFORE calling the LLM.
    Returns a validation dict:
      - flags: list of warning strings shown in UI
      - blocked: if True, skip LLM and return canned message
      - block_reason: canned output when blocked
    """
    stats   = result["raw_stats"]
    intent  = result["intent"]
    flags   = []
    blocked = False
    block_reason = ""

    # ── Marketing correlation guard ──────────────────────────
    if intent in ("MARKETING_IMPACT", "GENERAL_INSIGHTS"):
        corr = abs(stats.get("correlation", 0))
        if corr < CORR_WEAK:
            flags.append(
                f"⚠️ Correlation between marketing spend and sales is very weak "
                f"(r = {stats.get('correlation', 0):.4f}). "
                "No strong relationship observed in this dataset."
            )
            if intent == "MARKETING_IMPACT":
                blocked = True
                block_reason = (
                    f"No strong relationship observed between marketing spend and "
                    f"monthly sales (Pearson r = {stats.get('correlation', 0):.4f}). "
                    "The data does not support a meaningful causal conclusion."
                )

    if intent == "TIME_TREND":
        flags.append("Time-based analysis is not available in the current dataset.")
        blocked = True
        block_reason = "Time-based analysis is not available in the current dataset"
        return {"flags": flags, "blocked": blocked, "block_reason": block_reason}

    # ── Category difference guard ────────────────────────────
    rel_diff = stats.get("relative_diff", 1.0)
    if intent in ("SALES_TREND", "ROI_ANALYSIS", "GENERAL_INSIGHTS") and rel_diff < DIFF_THRESHOLD:
        flags.append(
            f"⚠️ Difference between top and bottom categories is very small "
            f"({rel_diff*100:.2f}%). No significant difference across categories."
        )
        blocked = True
        block_reason = (
            f"No significant difference detected across categories "
            f"(max relative spread = {rel_diff*100:.2f}%). "
            "Insufficient variation to draw a reliable conclusion."
        )

    return {"flags": flags, "blocked": blocked, "block_reason": block_reason}


def compute_confidence(result: dict) -> dict:
    """
    Returns {'level': 'High'|'Medium'|'Low', 'reason': str, 'score': float}
    """
    stats  = result["raw_stats"]
    intent = result["intent"]

    if intent == "MARKETING_IMPACT":
        corr  = abs(stats.get("correlation", 0))
        score = corr
        if corr >= CORR_STRONG:
            return {"level": "High",   "score": score,
                    "reason": f"Strong correlation (r={stats['correlation']:.4f})"}
        elif corr >= CORR_MODERATE:
            return {"level": "Medium", "score": score,
                    "reason": f"Moderate correlation (r={stats['correlation']:.4f})"}
        else:
            return {"level": "Low",    "score": score,
                    "reason": f"Weak correlation (r={stats['correlation']:.4f}) — trend unreliable"}

    elif intent in ("SALES_TREND", "ROI_ANALYSIS", "GENERAL_INSIGHTS",
                    "REGION_ANALYSIS", "CHANNEL_ANALYSIS",
                    "CAMPAIGN_ANALYSIS", "TIME_TREND"):
        rel_diff = stats.get("relative_diff", 0)
        group_label = {
            "REGION_ANALYSIS":   "regions",
            "CHANNEL_ANALYSIS":  "channels",
            "CAMPAIGN_ANALYSIS": "campaign types",
            "TIME_TREND":        "months",
        }.get(intent, "categories")
        score = min(rel_diff * 5, 1.0)
        if rel_diff >= 0.30:
            return {"level": "High",   "score": score,
                    "reason": f"Large spread between {group_label} ({rel_diff*100:.1f}%)"}
        elif rel_diff >= 0.10:
            return {"level": "Medium", "score": score,
                    "reason": f"Moderate spread between {group_label} ({rel_diff*100:.1f}%)"}
        else:
            return {"level": "Low",    "score": score,
                    "reason": f"Small spread between {group_label} ({rel_diff*100:.1f}%) — interpret with caution"}

    return {"level": "Low", "score": 0.0, "reason": "Insufficient signal for confidence scoring"}


def generate_base_insight(result: dict, confidence: dict) -> str:
    """
    Pure Python template insight — grounded 100% in computed numbers.
    This is shown even when LLM is unavailable.
    """
    stats  = result["raw_stats"]
    intent = result["intent"]

    if intent == "SALES_TREND":
        lines = [
            f"**{stats['top_category']}** leads with the highest average monthly sales "
            f"of **${stats['top_value']:,.2f}**, while **{stats['lowest_category']}** "
            f"has the lowest at **${stats['lowest_value']:,.2f}** "
            f"(difference: **${stats['difference']:,.2f}**).",
        ]
        if stats["num_categories"] > 2:
            ranked = sorted(stats["all_values"].items(), key=lambda x: x[1], reverse=True)
            ranking_str = " › ".join(f"{cat} (${val:,.0f})" for cat, val in ranked)
            lines.append(f"Ranking: {ranking_str}.")
        return " ".join(lines)

    elif intent == "MARKETING_IMPACT":
        corr   = stats["correlation"]
        slope  = stats["slope"]
        direction = "positive" if corr >= 0 else "negative"
        strength  = ("strong" if abs(corr) >= CORR_STRONG else
                     "moderate" if abs(corr) >= CORR_MODERATE else "weak")
        return (
            f"Marketing spend and monthly sales have a **{strength} {direction} correlation** "
            f"(r = **{corr:.4f}**). "
            f"Each additional unit of marketing spend is associated with "
            f"**${slope:,.4f}** change in monthly sales."
        )

    elif intent == "ROI_ANALYSIS":
        lines = [
            f"**{stats['top_category']}** achieves the highest average ROI of **{stats['top_value']:.4f}**, "
            f"versus **{stats['lowest_category']}** at **{stats['lowest_value']:.4f}** "
            f"(difference: **{stats['difference']:.4f}**).",
        ]
        if stats["num_categories"] > 2:
            ranked = sorted(stats["all_values"].items(), key=lambda x: x[1], reverse=True)
            ranking_str = " › ".join(f"{cat} ({val:.4f})" for cat, val in ranked)
            lines.append(f"ROI ranking: {ranking_str}.")
        return " ".join(lines)

    elif intent == "REGION_ANALYSIS":
        return f"{stats['top_category']} has highest sales with an average of ${stats['top_value']:,.2f}."

    elif intent == "CHANNEL_ANALYSIS":
        return f"{stats['top_category']} provides highest ROI with an average of {stats['top_value']:.4f}."

    elif intent == "CAMPAIGN_ANALYSIS":
        return f"{stats['top_category']} performs best with an average ROI of {stats['top_value']:.4f}."

    elif intent == "TIME_TREND":
        return "Time-based analysis is not available in the current dataset"

    else:  # GENERAL
        corr = stats.get("correlation", 0)
        return (
            f"Highest average monthly sales: **{stats['top_category']}** "
            f"(**${stats['top_value']:,.2f}**). "
            f"Lowest: **{stats['lowest_category']}** (**${stats['lowest_value']:,.2f}**)."
            f" Best ROI category: **{stats['best_roi_cat']}** (ROI = **{stats['best_roi_val']:.4f}**)."
            f" Marketing-to-sales correlation across all records: **{corr:.4f}**."
        )


