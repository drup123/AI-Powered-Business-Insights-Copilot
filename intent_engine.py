INTENT_RULES = {
    "REGION_ANALYSIS": [
        "region", "location", "area", "geography",
    ],
    "CHANNEL_ANALYSIS": [
        "channel", "platform", "ads", "marketing channel",
    ],
    "CAMPAIGN_ANALYSIS": [
        "campaign", "campaign type",
    ],
    "TIME_TREND": [
        "month", "season", "time", "monthly trend", "over time", "trend", "quarter",
    ],
    "SALES_TREND": [
        "sales", "revenue", "drop", "decline", "growth",
        "perform", "best sell", "worst sell",
    ],
    "MARKETING_IMPACT": [
        "marketing", "spend", "advertis", "affect", "impact",
        "correlat", "influence", "budget",
    ],
    "ROI_ANALYSIS": [
        "roi", "return", "profit", "efficient", "best roi",
        "highest return", "value", "invest",
    ],
    "GENERAL_INSIGHTS": [],   # fallback
}

# Topics that are completely outside the dataset
OUT_OF_SCOPE_KEYWORDS = [
    "weather", "stock", "employee", "headcount", "salary", "competitor",
    "social media", "customer satisfaction", "nps", "traffic", "website",
    "inventory", "supply chain", "inflation", "gdp",
]


def detect_intent(query: str) -> str:
    q = query.lower()
    # Out-of-scope check first
    if any(kw in q for kw in OUT_OF_SCOPE_KEYWORDS):
        return "OUT_OF_SCOPE"
    for intent, keywords in INTENT_RULES.items():
        if intent == "GENERAL_INSIGHTS":
            continue
        if any(kw in q for kw in keywords):
            return intent
    return "GENERAL_INSIGHTS"

