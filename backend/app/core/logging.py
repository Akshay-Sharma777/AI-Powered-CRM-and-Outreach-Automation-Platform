"""
Structured Logging and Correlation ID Middleware.
Outputs structured JSON logs and redacts sensitive contact data & tokens.
"""

import json
import logging
import re
import uuid
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Redaction patterns for sensitive information
EMAIL_REGEX = re.compile(r'([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')
BEARER_REGEX = re.compile(r'Bearer\s+[A-Za-z0-9\-._~+/]+=*')


def mask_sensitive_data(message: str) -> str:
    """Masks email addresses, bearer tokens, and secrets."""
    if not isinstance(message, str):
        return message
    # Mask emails: j***@domain.com
    masked = EMAIL_REGEX.sub(lambda m: f"{m.group(1)[:1]}***@{m.group(2)}", message)
    # Mask bearer tokens
    masked = BEARER_REGEX.sub("Bearer [REDACTED_TOKEN]", masked)
    return masked


class JSONLogFormatter(logging.Formatter):
    """Formats log records as structured JSON lines."""
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": mask_sensitive_data(record.getMessage()),
            "correlation_id": getattr(record, "correlation_id", None)
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def setup_logging():
    """Configures root logger with JSONLogFormatter."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONLogFormatter())
    root_logger.handlers = [handler]


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware that extracts or generates X-Correlation-ID for every incoming request
    and attaches it to the response header.
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        corr_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = corr_id

        # Process request
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = corr_id
        return response
