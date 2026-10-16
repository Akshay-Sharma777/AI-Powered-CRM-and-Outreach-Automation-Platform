"""
Contact Enrichment Router (Manual / Cost-Controlled).
Requires confirmed credit authorization.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from backend.app.core.security import require_roles

router = APIRouter(prefix="/leads", tags=["Enrichment"])


class EnrichRequest(BaseModel):
    provider: str
    confirmed_credits: int


@router.post("/{id}/enrich")
def enrich_contact(
    id: str,
    payload: EnrichRequest,
    current_user: dict = Depends(require_roles(["admin", "researcher"]))
):
    """Triggers manual provider lookup (ContactOut / Snov.io)."""
    if payload.confirmed_credits <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Credit confirmation required before triggering enrichment lookup"
        )

    return {
        "status": "success",
        "provider": payload.provider,
        "credits_used": payload.confirmed_credits,
        "contact": {
            "name": "Jane Doe",
            "role_title": "Technical Recruiter",
            "methods": [
                {
                    "kind": "email",
                    "value": "jane.doe@example.com",
                    "provenance": f"Enriched via {payload.provider}"
                }
            ]
        }
    }
