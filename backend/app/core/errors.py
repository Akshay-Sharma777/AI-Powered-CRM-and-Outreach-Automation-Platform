"""
Standard Custom Exceptions and Error Models.
Ensures error outputs strictly follow contracts/openapi.yaml.
"""

from typing import Optional
from fastapi import HTTPException, status


class PlatformError(HTTPException):
    def __init__(self, status_code: int, code: str, message: str, correlation_id: Optional[str] = None):
        super().__init__(
            status_code=status_code,
            detail={
                "status": status_code,
                "code": code,
                "message": message,
                "correlation_id": correlation_id
            }
        )


class ResourceNotFoundError(PlatformError):
    def __init__(self, resource: str, identifier: str, correlation_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="RESOURCE_NOT_FOUND",
            message=f"{resource} with id '{identifier}' was not found.",
            correlation_id=correlation_id
        )


class ConflictError(PlatformError):
    def __init__(self, message: str, correlation_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="RESOURCE_CONFLICT",
            message=message,
            correlation_id=correlation_id
        )


class BudgetExceededError(PlatformError):
    def __init__(self, provider: str, correlation_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="BUDGET_EXCEEDED",
            message=f"Credit limit exceeded for provider '{provider}'. Please review budget allocation.",
            correlation_id=correlation_id
        )


class PreSendCheckFailedError(PlatformError):
    def __init__(self, reason: str, correlation_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="PRE_SEND_VALIDATION_FAILED",
            message=f"Outreach blocked: {reason}",
            correlation_id=correlation_id
        )
