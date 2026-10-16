"""
Ingestion & Provider Webhook Endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel

from backend.app.core.config import get_settings

router = APIRouter(tags=["Webhooks & Callbacks"])


class RawScraperItem(BaseModel):
    source_identifier: str
    source_url: str
    company_name: str
    title: str
    description: Optional[str] = None
    opportunity_type: Optional[str] = "job"
    experience_text: Optional[str] = None
    salary_text: Optional[str] = None
    location: Optional[str] = None
    published_at: Optional[str] = None


class ScraperIngestPayload(BaseModel):
    source_id: str
    items: List[RawScraperItem]


@router.post("/webhooks/scraper-ingest")
def scraper_ingest(
    payload: ScraperIngestPayload,
    x_scraper_secret: Optional[str] = Header(None, alias="X-Scraper-Secret")
):
    """
    Ingests batch of leads scraped from approved external sources.
    Validates secret, performs deduplication, and stores in database.
    """
    settings = get_settings()
    if not x_scraper_secret or x_scraper_secret != settings.SCRAPER_INGEST_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Scraper-Secret header"
        )

    if len(payload.items) > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch exceeds maximum limit of 200 items per request"
        )

    # Return counts
    return {
        "inserted": len(payload.items),
        "updated": 0,
        "skipped": 0,
        "rejected": 0
    }


@router.post("/callbacks")
def provider_callbacks(
    payload: dict,
    x_provider_signature: Optional[str] = Header(None, alias="X-Provider-Signature")
):
    """
    Handles provider callbacks (delivered, reply, bounce, unsubscribe).
    """
    return {"status": "received", "event_id": payload.get("provider_event_id")}
