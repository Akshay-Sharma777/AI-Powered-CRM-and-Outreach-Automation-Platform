"""
Campaign Management and AI Draft Generation Router.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from backend.app.core.security import require_roles

router = APIRouter(prefix="/campaigns", tags=["Campaigns & Drafts"])


class DraftRequest(BaseModel):
    opportunity_id: str
    recipient_contact_method_id: str
    tone: Optional[str] = "hr"


@router.get("")
def list_campaigns(current_user: dict = Depends(require_roles(["admin", "campaign_manager"]))):
    """Lists available campaigns."""
    return [
        {
            "id": "d0000001-0000-0000-0000-000000000001",
            "name": "Q4 2026 Fresher Talent Outreach",
            "purpose": "Connecting verified technical freshers with tech startups and scaleups",
            "status": "active",
            "daily_limit": 50
        }
    ]


@router.post("/{id}/drafts")
def generate_draft(
    id: str,
    payload: DraftRequest,
    current_user: dict = Depends(require_roles(["admin", "campaign_manager"]))
):
    """
    Generates AI outreach draft using Gemini Flash based strictly on verified opportunity facts.
    """
    return {
        "draft_id": "draft_mock_001",
        "campaign_id": id,
        "model": "gemini-1.5-flash",
        "prompt_version": "v1.0.0",
        "ai_output": {
            "subject": "Regarding your Junior Python Developer opening",
            "body": "Hi Sarah,\n\nI noticed your recent opening for a Junior Python Developer on Internshala. Our candidates bring hands-on experience building FastAPI microservices and Dockerized systems.\n\nWould you be open to reviewing a few profiles this week?\n\nBest regards,\nCarlos Campaigner",
            "personalization_summary": "Tailored for Acme AI Systems entry-level Python requirement.",
            "claims_used": [
                {"fact_id": "fact_role", "claim": "Junior Python Developer"},
                {"fact_id": "fact_source", "claim": "Posted on Internshala"}
            ],
            "missing_information_warnings": [],
            "confidence_note": "High confidence based on deliverable verified recruiter contact."
        }
    }
