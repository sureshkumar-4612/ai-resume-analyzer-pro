"""
LLM Client — OpenRouter API Integration
────────────────────────────────────────
Provides a thin wrapper around the OpenRouter chat/completions
endpoint using the deepseek/deepseek-r1:free model.

Used by every tool that requires LLM inference.
"""

import re
import httpx  # type: ignore[import-untyped]
from config import (  # type: ignore[import-untyped]
    OPENROUTER_API_KEY,
    OPENROUTER_CHAT_ENDPOINT,
    MODEL_NAME,
    MODEL_TEMPERATURE,
    MODEL_MAX_TOKENS,
)


def call_llm(prompt: str, *, temperature: float | None = None, max_tokens: int | None = None) -> str:
    """
    Send a single-turn prompt to DeepSeek R1 via OpenRouter
    and return the assistant's response text.
    """
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_openrouter_api_key_here":
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. "
            "Create a .env file with your key (see .env.example)."
        )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/ai-resume-analyzer",
        "X-Title": "AI Resume Analyzer Agent",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature if temperature is not None else MODEL_TEMPERATURE,
        "max_tokens": max_tokens if max_tokens is not None else MODEL_MAX_TOKENS,
    }

    response = httpx.post(
        OPENROUTER_CHAT_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=90.0,
    )
    response.raise_for_status()

    data = response.json()

    # Extract the assistant message content
    content = data["choices"][0]["message"]["content"]

    # DeepSeek R1 may wrap its answer in <think>…</think> tags.
    # Strip the thinking block and return only the final answer.
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

    return content
