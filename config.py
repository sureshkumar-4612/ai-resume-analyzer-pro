"""
Configuration module for AI Resume Analyzer Agent.

Loads environment variables and defines model / API settings
as specified in the project requirements.
"""

import os
from dotenv import load_dotenv  # type: ignore[import-untyped]

# ── Load .env ────────────────────────────────────────────────
load_dotenv()

# ── OpenRouter API ───────────────────────────────────────────
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
OPENROUTER_CHAT_ENDPOINT: str = "https://openrouter.ai/api/v1/chat/completions"

# ── Model Configuration ─────────────────────────────────────
MODEL_NAME: str = "openrouter/free"
MODEL_TEMPERATURE: float = 0.2
MODEL_MAX_TOKENS: int = 4000

# ── Application Settings ────────────────────────────────────
SUPPORTED_EXTENSIONS: list[str] = [".pdf", ".txt", ".md"]
MAX_PROCESSING_TIME_SECONDS: int = 10
