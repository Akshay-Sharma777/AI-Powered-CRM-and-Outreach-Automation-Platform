"""
Suppression & Do-Not-Contact Management Router.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from backend.app.core.security import require_roles

router = APIRouter(prefix="/suppression", tags=["Suppression"])


class CreateSuppressionEntry(BaseModel):
    value: str
    kind: str
    reason: str


SUPPRESSION_LIST = [
    {
        "id": "s0000001-0000-0000-0000-000000000001",
        "value": "blocked-company.example.com",
        "kind": "domain",
        "reason": "Organization requested no cold contact",
        "created_at": "2026-10-15T00:00:00Z"
    },
    {
        "id": "s0000002-0000-0000-0000-000000000002",
        "value": "optout@example.com",
        "kind": "email",
        "reason": "Recipient clicked unsubscribe",
        "created_at": "2026-10-15T00:00:00Z"
    }
]


@router.get("")
def list_suppressions(current_user: dict = Depends(require_roles(["admin", "campaign_manager", "researcher"]))):
    """Lists blocked emails and domains."""
    return SUPPRESSION_LIST


@router.post("", status_code=status.HTTP_201_CREATED)
def add_suppression(
    payload: CreateSuppressionEntry,
    current_user: dict = Depends(require_roles(["admin", "campaign_manager"]))
):
    """Adds email or domain to suppression list."""
    val_lower = payload.value.lower().strip()
    for item in SUPPRESSION_LIST:
        if item["value"].lower() == val_lower and item["kind"] == payload.kind:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Entry '{payload.value}' is already suppressed"
            )

    new_entry = {
        "id": f"s_mock_{len(SUPPRESSION_LIST) + 1}",
        "value": val_lower,
        "kind": payload.kind,
        "reason": payload.reason,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    SUPPRESSION_LIST.append(new_entry)
    return new_entry
