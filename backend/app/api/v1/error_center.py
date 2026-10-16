"""
Error Center and Guardrail Webhook Router.
"""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from backend.app.core.security import require_roles

router = APIRouter(tags=["Error Center & Guardrails"])


class ErrorWebhookPayload(BaseModel):
    workflow: str
    job_id: str
    correlation_id: str
    failed_step: str
    category: str
    redacted_message: str
    retry_count: int = 0
    next_retry_at: Optional[str] = None
    owner: str = "automation"
    replay_eligible: bool = True
    payload_snapshot: Optional[dict] = None


SAMPLE_ERRORS = [
    {
        "id": "err_001",
        "workflow": "daily_discovery",
        "job_id": "job_sample_01",
        "correlation_id": "corr_c8f2b730-811c",
        "failed_step": "fetch_naukri_listings",
        "category": "rate_limit",
        "redacted_message": "HTTP 429 Too Many Requests received from target source",
        "retry_count": 2,
        "next_retry_at": "2026-10-16T14:30:00Z",
        "owner": "automation",
        "replay_eligible": True,
        "ai_suggestion": "Target rate limited requests. Increase backoff window or reduce concurrency.",
        "status": "open"
    }
]


@router.post("/guardrails/error-webhook")
def record_automation_error(payload: ErrorWebhookPayload):
    """Ingests error occurrences from n8n and scraper workers."""
    replay_eligible = payload.replay_eligible
    # Send timeouts and provider rejections cannot be replayed blindly
    if payload.category in ["send_timeout", "permanent_provider_rejection"]:
        replay_eligible = False

    error_record = payload.model_dump()
    error_record["id"] = f"err_{len(SAMPLE_ERRORS) + 1:03d}"
    error_record["replay_eligible"] = replay_eligible
    error_record["status"] = "open"
    SAMPLE_ERRORS.append(error_record)
    return {"status": "recorded", "error_id": error_record["id"]}


@router.get("/error_center")
def list_errors(current_user: dict = Depends(require_roles(["admin", "developer"]))):
    """Lists recent system and automation errors."""
    return SAMPLE_ERRORS


@router.post("/error_center/{id}/replay")
def replay_error(id: str, current_user: dict = Depends(require_roles(["admin", "developer"]))):
    """Triggers retry of a failed job if replay eligible."""
    for err in SAMPLE_ERRORS:
        if err["id"] == id:
            if not err["replay_eligible"]:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This error category is not eligible for automated replay. Manual reconciliation required."
                )
            err["status"] = "retrying"
            return {"status": "replay_queued", "error_id": id}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error record not found")
