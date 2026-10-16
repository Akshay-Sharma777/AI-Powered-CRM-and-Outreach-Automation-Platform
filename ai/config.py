"""
AI Configuration Module.
Reads Gemini API configuration from environment variables.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AIConfig:
    gemini_api_key: Optional[str]
    gemini_model: str
    timeout_seconds: int
    mock_mode: bool


def get_ai_config() -> AIConfig:
    """Loads AI configuration from environment variables."""
    return AIConfig(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        timeout_seconds=int(os.getenv("GEMINI_TIMEOUT_SECONDS", "30")),
        mock_mode=os.getenv("GEMINI_MOCK_MODE", "true").lower() in ("true", "1", "yes")
    )
