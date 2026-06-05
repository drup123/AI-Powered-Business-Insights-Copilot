from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # ── API ──────────────────────────────────────────────────
    app_name: str = "AI-Powered Business Insights Copilot"
    app_version: str = "1.0.0"
    debug: bool = False

    # ── Groq LLM ─────────────────────────────────────────────
    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"

    # ── Dataset ───────────────────────────────────────────────
    dataset_path: str = "improved_business_dataset.csv"

    # ── Analysis thresholds ───────────────────────────────────
    corr_strong: float = 0.6
    corr_moderate: float = 0.3
    corr_weak: float = 0.2
    diff_threshold: float = 0.05

    # ── CORS ──────────────────────────────────────────────────
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
