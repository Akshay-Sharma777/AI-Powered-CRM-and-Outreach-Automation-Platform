"""
Gemini Flash Client Wrapper.
Handles API requests, rate-limiting backoff, token tracking, and offline test mocks.
"""

import json
import logging
import time
from typing import Optional, Dict, Any, Tuple
from ai.config import get_ai_config

logger = logging.getLogger(__name__)


class GeminiClient:
    def __init__(self, config=None):
        self.config = config or get_ai_config()

    def generate(
        self,
        prompt: str,
        schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.3
    ) -> Tuple[Dict[str, Any], Dict[str, int]]:
        """
        Generates text using Google Gemini Flash model.
        Returns: (parsed_json_output, token_usage_dict)
        """
        # If running in mock mode or API key is not set, return compliant canned output
        if self.config.mock_mode or not self.config.gemini_api_key:
            logger.info("GeminiClient running in mock mode; returning offline fixture.")
            mock_payload = {
                "subject": "Regarding your entry-level opening",
                "body": "Hi there,\n\nI saw your verified job listing for the software engineer position. Our interns have proven skills in Python, FastAPI, and direct SQL workflows.\n\nBest regards,\nOutreach Team",
                "personalization_summary": "Generated using verified listing attributes.",
                "claims_used": [
                    {"fact_id": "fact_01", "claim": "Software engineer role"}
                ],
                "missing_information_warnings": [],
                "confidence_note": "Mock generated response compliant with draft schema."
            }
            usage = {"prompt_tokens": 120, "completion_tokens": 65, "total_tokens": 185}
            return mock_payload, usage

        # Real API request with retry logic (using google-genai or httpx)
        # Bounded exponential backoff on 429 / 5xx
        import httpx
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.gemini_model}:generateContent?key={self.config.gemini_api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "responseMimeType": "application/json"
            }
        }

        attempts = 3
        delay = 1.0
        for attempt in range(1, attempts + 1):
            try:
                with httpx.Client(timeout=self.config.timeout_seconds) as client:
                    resp = client.post(url, headers=headers, json=payload)
                    if resp.status_code in (429, 500, 502, 503, 504):
                        if attempt < attempts:
                            time.sleep(delay)
                            delay *= 2
                            continue
                    resp.raise_for_status()
                    data = resp.json()
                    text_content = data["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(text_content)
                    usage = {
                        "prompt_tokens": data.get("usageMetadata", {}).get("promptTokenCount", 0),
                        "completion_tokens": data.get("usageMetadata", {}).get("candidatesTokenCount", 0),
                        "total_tokens": data.get("usageMetadata", {}).get("totalTokenCount", 0)
                    }
                    return parsed, usage
            except Exception as e:
                if attempt >= attempts:
                    logger.error("Gemini request failed after %d attempts: %s", attempts, e)
                    raise e
                time.sleep(delay)
                delay *= 2
