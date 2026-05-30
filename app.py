"""
AI-Powered Business Insights Copilot  —  v2 (Controlled Hybrid)
=================================================================
Architecture:
  Pandas  → ALL calculations (truth layer)
  Python  → decision logic + guardrails + template insights
  Groq    → ONLY human-readable explanation (no reasoning beyond data)

Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd

from config import GROQ_API_KEY, GROQ_MODEL, DATASET_PATH, CORR_WEAK, DIFF_THRESHOLD
from data_layer import load_data
from intent_engine import detect_intent
from analysis_engine import process_query, validate_result, compute_confidence, generate_base_insight
from llm_layer import build_structured_summary, generate_insight
from visualizations import plot_visuals

# ─────────────────────────────────────────────────────────────
# PAGE SETUP
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Business Insights Copilot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS  — premium dark theme
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0d0f1a 0%, #111827 50%, #0d1117 100%);
    color: #e2e8f0;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #0d1117 100%);
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* KPI cards */
.kpi-grid { display:flex; gap:1rem; margin-bottom:1.5rem; flex-wrap:wrap; }
.kpi-card {
    flex:1; min-width:150px;
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border:1px solid #334155; border-radius:16px;
    padding:1.2rem 1.5rem; text-align:center;
    box-shadow:0 4px 24px rgba(0,0,0,.4);
    transition:transform .2s, box-shadow .2s;
}
.kpi-card:hover { transform:translateY(-3px); box-shadow:0 8px 32px rgba(99,102,241,.2); }
.kpi-value {
    font-size:1.9rem; font-weight:700;
    background:linear-gradient(135deg,#818cf8,#38bdf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.kpi-label { font-size:.78rem; color:#94a3b8; text-transform:uppercase; letter-spacing:.08em; margin-top:.3rem; }

/* Chat bubbles */
.chat-user { display:flex; justify-content:flex-end; margin:.6rem 0; }
.chat-user .bubble {
    background:linear-gradient(135deg,#6366f1,#4f46e5);
    color:#fff; border-radius:18px 18px 4px 18px;
    padding:.7rem 1.1rem; max-width:70%;
    font-size:.92rem; box-shadow:0 2px 12px rgba(99,102,241,.3);
}
.chat-ai { display:flex; justify-content:flex-start; margin:.6rem 0; gap:.6rem; }
.chat-ai .avatar {
    width:34px; height:34px; border-radius:50%;
    background:linear-gradient(135deg,#0ea5e9,#6366f1);
    display:flex; align-items:center; justify-content:center;
    font-size:1rem; flex-shrink:0;
}
.chat-ai .bubble {
    background:#1e293b; border:1px solid #334155; color:#e2e8f0;
    border-radius:4px 18px 18px 18px;
    padding:.7rem 1.1rem; max-width:75%;
    font-size:.92rem; box-shadow:0 2px 8px rgba(0,0,0,.3);
}

/* Result panels */
.panel-box {
    border-radius:12px; padding:1rem 1.2rem; margin-top:.8rem;
}
.base-insight-box {
    background:rgba(56,189,248,.08); border:1px solid rgba(56,189,248,.3);
}
.llm-insight-box {
    background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(56,189,248,.08));
    border:1px solid rgba(99,102,241,.35);
}
.explain-box {
    background:rgba(16,185,129,.07); border:1px solid rgba(16,185,129,.28);
}
.guardrail-box {
    background:rgba(251,146,60,.08); border:1px solid rgba(251,146,60,.35);
}
.panel-label {
    font-size:.72rem; font-weight:700; text-transform:uppercase;
    letter-spacing:.1em; margin-bottom:.45rem;
}
.base-label   { color:#38bdf8; }
.llm-label    { color:#818cf8; }
.explain-label{ color:#34d399; }
.guard-label  { color:#fb923c; }

/* Quick buttons */
.stButton > button {
    background:linear-gradient(135deg,#1e293b,#0f172a) !important;
    color:#818cf8 !important; border:1px solid #334155 !important;
    border-radius:20px !important; font-size:.82rem !important;
    padding:.35rem .9rem !important; transition:all .2s !important;
}
.stButton > button:hover {
    background:linear-gradient(135deg,#6366f1,#4f46e5) !important;
    color:#fff !important; border-color:#6366f1 !important;
    transform:translateY(-1px) !important;
}

[data-testid="stDataFrame"] { border-radius:10px; overflow:hidden; }
hr { border-color:#1e293b !important; }
[data-testid="stTextInput"] input {
    background:#1e293b !important; color:#e2e8f0 !important;
    border:1px solid #334155 !important; border-radius:10px !important;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# UI HELPERS
# ═══════════════════════════════════════════════════════════════

def render_kpis(df: pd.DataFrame):
    avg_sales    = df["monthly_sales"].mean()
    avg_spend    = df["marketing_spend"].mean()
    roi_by_cat   = df.groupby("Category")["ROI"].mean()
    best_roi_cat = roi_by_cat.idxmax()
    best_roi_val = roi_by_cat.max()
    corr_val     = df["marketing_spend"].corr(df["monthly_sales"])

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-value">${avg_sales:,.0f}</div>
            <div class="kpi-label">Avg Monthly Sales</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">${avg_spend:,.0f}</div>
            <div class="kpi-label">Avg Marketing Spend</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{best_roi_cat}</div>
            <div class="kpi-label">Best ROI Category</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{best_roi_val:.3f}</div>
            <div class="kpi-label">Highest Avg ROI</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{corr_val:.3f}</div>
            <div class="kpi-label">Mktg–Sales Correlation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_message(role: str, content: str):
    if role == "user":
        st.markdown(f"""
        <div class="chat-user"><div class="bubble">{content}</div></div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-ai">
          <div class="avatar">🧠</div>
          <div class="bubble">{content}</div>
        </div>""", unsafe_allow_html=True)


def intent_badge_html(intent: str) -> str:
    badges = {
        "SALES_TREND":      ("📈", "Sales Trend",        "#6366f1"),
        "MARKETING_IMPACT": ("📣", "Marketing Impact",   "#38bdf8"),
        "ROI_ANALYSIS":     ("💰", "ROI Analysis",       "#34d399"),
        "GENERAL_INSIGHTS": ("🔍", "General Overview",   "#fb923c"),
        "REGION_ANALYSIS":  ("🌍", "Region Analysis",    "#a78bfa"),
        "CHANNEL_ANALYSIS": ("📢", "Channel Analysis",   "#f472b6"),
        "CAMPAIGN_ANALYSIS":("🎯", "Campaign Analysis",  "#facc15"),
        "TIME_TREND":       ("📅", "Time Trend",         "#34d399"),
        "OUT_OF_SCOPE":     ("🚫", "Out of Scope",       "#ef4444"),
    }
    icon, label, color = badges.get(intent, ("🔍", "Insight", "#94a3b8"))
    return (
        f'<span style="background:{color}22;color:{color};border:1px solid {color}55;'
        f'border-radius:20px;padding:.2rem .75rem;font-size:.76rem;font-weight:700;">'
        f'{icon} {label}</span>'
    )


def render_result_card(entry: dict):
    result       = entry["result"]
    base_insight = entry["base_insight"]
    llm_out      = entry["llm"]
    validation   = entry["validation"]
    bar_fig      = entry["bar_fig"]
    scatter_fig  = entry["scatter_fig"]
    intent       = result["intent"]

    # Header
    titles = {
        "SALES_TREND":      "Sales Trend Analysis",
        "MARKETING_IMPACT": "Marketing Impact Analysis",
        "ROI_ANALYSIS":     "ROI Analysis",
        "GENERAL_INSIGHTS": "Business Overview",
        "REGION_ANALYSIS":  "Region Performance Analysis",
        "CHANNEL_ANALYSIS": "Marketing Channel Analysis",
        "CAMPAIGN_ANALYSIS":"Campaign Type Analysis",
        "TIME_TREND":       "Monthly Sales Trend",
    }
    st.markdown(
        f"<div style='margin:.5rem 0 .8rem;'>"
        f"{intent_badge_html(intent)}&nbsp;&nbsp;"
        f"<span style='font-size:1.1rem;font-weight:600;color:#e2e8f0;'>{titles.get(intent,'Analysis')}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Guardrail warnings ──────────────────────────────────
    if validation["flags"]:
        for flag in validation["flags"]:
            st.markdown(f"""
            <div class="panel-box guardrail-box">
              <div class="panel-label guard-label">⚠️ Data Guardrail</div>
              <p style="margin:0;color:#fdba74;font-size:.9rem;">{flag}</p>
            </div>""", unsafe_allow_html=True)

    # If blocked by guardrail, show canned message and stop
    if validation["blocked"]:
        st.markdown(f"""
        <div class="panel-box guardrail-box" style="margin-top:.5rem;">
          <div class="panel-label guard-label">🚫 Insight Blocked</div>
          <p style="margin:0;color:#fdba74;">{validation['block_reason']}</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("**📋 Raw Data (for reference)**")
        st.dataframe(result["table"], use_container_width=True, hide_index=True)
        return

    # ① Data table
    st.markdown("**📋 Data Results**")
    st.dataframe(result["table"], use_container_width=True, hide_index=True)

    # ② Charts
    tab1, tab2 = st.tabs(["📊 Bar Chart", "🔵 Scatter Plot"])
    with tab1:
        st.plotly_chart(bar_fig, use_container_width=True)
    with tab2:
        st.plotly_chart(scatter_fig, use_container_width=True)

    # ③ Base insight (Python template — data-grounded)
    st.markdown(f"""
    <div class="panel-box base-insight-box">
      <div class="panel-label base-label">📐 Data-Grounded Insight</div>
      <p style="margin:0;color:#e2e8f0;line-height:1.65;">{base_insight}</p>
    </div>""", unsafe_allow_html=True)

    # ④ LLM explanation
    st.markdown(f"""
    <div class="panel-box llm-insight-box">
      <div class="panel-label llm-label">💡 AI Explanation</div>
      <p style="margin:0;color:#e2e8f0;line-height:1.65;">{llm_out.get('explanation','—')}</p>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# MAIN APP ENTRY POINT
# ═══════════════════════════════════════════════════════════════

QUICK_QUESTIONS = [
    "Why did sales drop last quarter?",
    "Which region performs best?",
    "Which marketing channel gives best ROI?",
    "Which campaign type is most effective?",
    "What are the monthly sales trends?",
    "Give me a general business overview",
]

def main():
    # Session state
    for key, default in [("messages", []), ("results", [])]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ── Sidebar ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <h2 style='background:linear-gradient(135deg,#818cf8,#38bdf8);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                   font-size:1.4rem;margin-bottom:.2rem;'>🧠 Copilot v2</h2>
        <p style='color:#64748b;font-size:.82rem;margin-bottom:1.2rem;'>
        Controlled Hybrid Architecture
        </p>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**📂 Dataset**")
        df = load_data()
        if df is not None:
            st.success(f"✅ Loaded  •  {len(df):,} rows")
            st.markdown(f"**Categories:** {', '.join(sorted(df['Category'].unique()))}")
        else:
            st.error(f"❌ `{DATASET_PATH}` not found.")

        st.markdown("---")
        st.markdown("**📌 Supported Intents**")
        for label in [
            "📈 Sales Trend", "📣 Marketing Impact",
            "💰 ROI Analysis", "🔍 General Overview",
            "🌍 Region Analysis", "📢 Channel Analysis",
            "🎯 Campaign Analysis",
        ]:
            st.markdown(f"• {label}")

        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.results  = []
            st.rerun()

    # ── Dataset guard ────────────────────────────────────────
    if df is None:
        st.markdown("""
        <div style='text-align:center;padding:4rem 2rem;'>
          <div style='font-size:4rem;'>📂</div>
          <h2 style='color:#818cf8;'>Dataset Not Found</h2>
          <p style='color:#64748b;'>
            Place <code>improved_business_dataset.csv</code> in the same folder as <code>app.py</code>
            and refresh.
          </p>
        </div>""", unsafe_allow_html=True)
        return

    # ── Header ───────────────────────────────────────────────
    st.markdown("""
    <div style='text-align:center;padding:1.2rem 0 .8rem;'>
      <h1 style='background:linear-gradient(135deg,#818cf8,#38bdf8,#34d399);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 font-size:2.1rem;font-weight:700;margin-bottom:.35rem;'>
        🧠 Business Insights Copilot
      </h1>
      <p style='color:#64748b;font-size:.9rem;'>
        Pandas → Guardrails → Template Insight → Controlled LLM Explanation
      </p>
    </div>""", unsafe_allow_html=True)

    # ── KPIs ─────────────────────────────────────────────────
    render_kpis(df)
    st.markdown("---")

    # ── Chat history ─────────────────────────────────────────
    if not st.session_state.messages:
        st.markdown("""
        <div style='text-align:center;padding:1.5rem;color:#334155;'>
          <div style='font-size:2.8rem;'>💬</div>
          <p style='margin:.4rem 0 0;'>Ask a data question or pick a quick question below.</p>
        </div>""", unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            render_chat_message(msg["role"], msg["content"])

    st.markdown("---")

    # ── Quick questions (two rows of 3) ──────────────────────
    st.markdown("<p style='color:#64748b;font-size:.82rem;margin-bottom:.4rem;'>⚡ Quick Questions</p>",
                unsafe_allow_html=True)
    triggered_query = None
    row1, row2 = QUICK_QUESTIONS[:3], QUICK_QUESTIONS[3:]
    cols1 = st.columns(len(row1))
    for idx, (col, q) in enumerate(zip(cols1, row1)):
        with col:
            if st.button(q, key=f"quick_btn_{idx}"):
                triggered_query = q
    cols2 = st.columns(len(row2))
    for idx, (col, q) in enumerate(zip(cols2, row2)):
        with col:
            if st.button(q, key=f"quick_btn_{idx + len(row1)}"):
                triggered_query = q

    # ── Chat input ────────────────────────────────────────────
    with st.form("chat_form", clear_on_submit=True):
        c1, c2 = st.columns([5, 1])
        with c1:
            user_input = st.text_input(
                "query", label_visibility="collapsed",
                placeholder="e.g. Which category has the highest ROI?",
            )
        with c2:
            submitted = st.form_submit_button("Send ➤", use_container_width=True)

    query = triggered_query or (user_input.strip() if submitted and user_input.strip() else None)

    # ── Process pipeline ──────────────────────────────────────
    if query:
        st.session_state.messages.append({"role": "user", "content": query})

        with st.spinner("🔍 Running analysis pipeline..."):
            intent = detect_intent(query)

            # Out-of-scope fallback
            if intent == "OUT_OF_SCOPE":
                fallback_entry = {
                    "query":        query,
                    "result":       {"intent": "OUT_OF_SCOPE", "table": None, "raw_stats": {}},
                    "base_insight": "Insufficient data to answer this question.",
                    "llm":          {"explanation": ""},
                    "confidence":   {"level": "Low", "score": 0, "reason": "Topic not in dataset"},
                    "validation":   {"flags": [], "blocked": True,
                                     "block_reason": "This question references topics not present in the dataset (Category, monthly_sales, marketing_spend, ROI, Region, Marketing_Channel, Campaign_Type). Please ask a question about sales, marketing, ROI, regions, channels, campaigns, or monthly trends."},
                    "bar_fig":      None,
                    "scatter_fig":  None,
                }
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "⚠️ Insufficient data to answer this question.",
                })
                st.session_state.results.append(fallback_entry)
                st.rerun()

            # Normal pipeline
            result     = process_query(df, intent)
            validation = validate_result(result)
            confidence = compute_confidence(result)
            base_insight = generate_base_insight(result, confidence)

            # Only call LLM if not blocked
            if not validation["blocked"]:
                structured_summary = build_structured_summary(result, base_insight, confidence)
                llm_out = generate_insight(structured_summary, GROQ_API_KEY)
            else:
                llm_out = {"explanation": ""}

            bar_fig, scatter_fig = plot_visuals(df, result)

        st.session_state.messages.append({
            "role":    "assistant",
            "content": f"Analysis complete for: <em>{query}</em>",
        })
        st.session_state.results.append({
            "query":        query,
            "result":       result,
            "base_insight": base_insight,
            "llm":          llm_out,
            "validation":   validation,
            "bar_fig":      bar_fig,
            "scatter_fig":  scatter_fig,
        })
        st.rerun()

    # ── Render latest result ──────────────────────────────────
    if st.session_state.results:
        latest = st.session_state.results[-1]
        st.markdown("---")

        # Out-of-scope card
        if latest["result"]["intent"] == "OUT_OF_SCOPE":
            st.markdown(f"""
            <div style="background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.35);
                        border-radius:12px;padding:1rem 1.2rem;margin-top:.5rem;">
              <div style="color:#f87171;font-weight:700;margin-bottom:.4rem;">🚫 Out of Scope</div>
              <p style="margin:0;color:#fca5a5;">{latest['validation']['block_reason']}</p>
            </div>""", unsafe_allow_html=True)
        else:
            render_result_card(latest)

        # Previous analyses accordion
        if len(st.session_state.results) > 1:
            with st.expander(f"📜 Previous Analyses ({len(st.session_state.results)-1})"):
                for prev in reversed(st.session_state.results[:-1]):
                    st.markdown(f"**Q:** {prev['query']}")
                    if prev["result"]["table"] is not None:
                        st.dataframe(prev["result"]["table"],
                                     use_container_width=True, hide_index=True)
                    st.markdown(f"📐 {prev['base_insight']}")
                    st.markdown("---")

if __name__ == "__main__":
    main()
