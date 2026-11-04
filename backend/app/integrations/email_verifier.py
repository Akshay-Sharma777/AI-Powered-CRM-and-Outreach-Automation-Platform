
"""
Email deliverability verifier integration.

Sandbox mode returns an explicit unknown result.
Hunter API is used when sandbox mode is disabled.
"""

from typing import Any, Dict

import requests

from backend.app.core.config import get_settings


class EmailVerifierClient:
    """Client wrapper for email deliverability verification."""

    HUNTER_URL = "https://api.hunter.io/v2/email-verifier"

    def __init__(self) -> None:
        self.settings = get_settings()

    def verify(self, email: str) -> Dict[str, Any]:
        """Verify an email address using the configured provider."""

        # Sandbox never contacts an external provider.
        if self.settings.EMAIL_VERIFIER_SANDBOX:
            return {
                "result": "unknown",
                "raw_response": {
                    "mode": "sandbox",
                    "message": "No real email verification was performed.",
                },
            }

        provider = self.settings.EMAIL_VERIFIER_PROVIDER.lower()

        if provider != "hunter":
            raise NotImplementedError(
                f"Email verifier provider '{provider}' is not supported."
            )

        api_key = self.settings.EMAIL_VERIFIER_API_KEY

        if not api_key:
            raise NotImplementedError(
                "Hunter API key is not configured."
            )

        try:
            response = requests.get(
                self.HUNTER_URL,
                params={"email": email},
                headers={"X-API-KEY": api_key},
                timeout=25,
            )

            if response.status_code == 202:
                return {
                    "result": "unknown",
                    "raw_response": {
                        "provider": "hunter",
                        "status": "processing",
                        "http_status": 202,
                    },
                }

            try:
                payload = response.json()
            except ValueError:
                payload = {
                    "message": "Invalid JSON response from Hunter."
                }

            if response.status_code != 200:
                return {
                    "result": "failed",
                    "raw_response": {
                        "provider": "hunter",
                        "http_status": response.status_code,
                        "response": payload,
                    },
                }

            data = payload.get("data", {})
            hunter_status = data.get("status")

            status_mapping = {
                "valid": "deliverable",
                "invalid": "undeliverable",
                "accept_all": "catch_all",
                "unknown": "unknown",
                "webmail": "risky",
                "disposable": "risky",
            }

            allowed_results = {
                "deliverable",
                "undeliverable",
                "catch_all",
                "risky",
                "unknown",
            }

            hunter_result = data.get("result")

            if hunter_result in allowed_results:
                result = hunter_result
            else:
                result = status_mapping.get(
                    hunter_status,
                    "unknown",
                )

            return {
                "result": result,
                "raw_response": {
                    "provider": "hunter",
                    "response": payload,
                },
            }

        except requests.exceptions.RequestException as exc:
            return {
                "result": "failed",
                "raw_response": {
                    "provider": "hunter",
                    "error": type(exc).__name__,
                },
            }
