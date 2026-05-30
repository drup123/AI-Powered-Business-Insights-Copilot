import json
import hashlib
from groq import Groq
from config import GROQ_MODEL

def build_structured_summary(result: dict, base_insight: str, confidence: dict) -> str:
    """
    Creates a compact, numbers-only text block to send to the LLM.
    The LLM never sees the raw DataFrame.
    """
    stats  = result["raw_stats"]
    intent = result["intent"]

    lines = [
        f"INTENT: {intent}",
        f"BASE_INSIGHT: {base_insight}",
        f"CONFIDENCE: {confidence['level']} — {confidence['reason']}",
        "COMPUTED_VALUES:",
    ]

    for k, v in stats.items():
        if k == "all_values":
            lines.append(f"  category_ranking: " +
                         ", ".join(f"{cat}={val}" for cat, val in
                                   sorted(v.items(), key=lambda x: x[1], reverse=True)))
        elif isinstance(v, float):
            lines.append(f"  {k}: {v:.4f}")
        else:
            lines.append(f"  {k}: {v}")

    return "\n".join(lines)


_insight_cache: dict[str, dict] = {}

STRICT_SYSTEM_PROMPT = """You are a strict data analyst assistant.

RULES (non-negotiable):
1. ONLY use the numbers and facts provided in the DATA SUMMARY below.
2. Do NOT assume any external factors: no customer behavior, market trends, lifestyle changes, economic conditions, seasonal demand, or competitor activity.
3. Do NOT invent, modify, or extrapolate numbers.
4. If the data is insufficient or correlation is weak, say exactly: "Insufficient data to draw a strong conclusion."
5. Keep your explanation short (2-4 sentences), factual, and grounded only in what the numbers show.
6. Focus ONLY on: numerical comparisons, observed relationships, and data-visible patterns.

Respond in EXACTLY this JSON format — nothing else:
{
  "explanation": "..."
}"""


def generate_insight(structured_summary: str, api_key: str) -> dict:
    """
    Sends ONLY the structured summary to Groq.
    LLM job: explain the base insight in plain English — nothing more.
    """
    cache_key = hashlib.md5(structured_summary.encode()).hexdigest()
    if cache_key in _insight_cache:
        return _insight_cache[cache_key]

    if not api_key or api_key == "YOUR_GROQ_API_KEY_HERE":
        return {"explanation": "⚠️ No Groq API key configured."}

    user_msg = (
        "Here is the data summary. Write a strict, factual explanation "
        "based ONLY on these numbers:\n\n" + structured_summary
    )

    try:
        client   = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": STRICT_SYSTEM_PROMPT},
                {"role": "user",   "content": user_msg},
            ],
            temperature=0.1,   # near-deterministic
            max_tokens=256,
        )
        raw   = response.choices[0].message.content.strip()
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        parsed = json.loads(raw[start:end])
        out = {"explanation": parsed.get("explanation", raw)}
        _insight_cache[cache_key] = out
        return out

    except json.JSONDecodeError:
        out = {"explanation": raw}
        _insight_cache[cache_key] = out
        return out
    except Exception as e:
        return {"explanation": f"LLM unavailable: {e}"}

