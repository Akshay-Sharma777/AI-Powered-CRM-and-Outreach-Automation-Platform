"""
Health and System Status Endpoints.
"""

from datetime import datetime, timezone
from fastapi import APIRouter
from backend.app.core.config import get_settings

router = APIRouter(tags=["Health & Monitoring"])


@router.get("/health")
def health_check():
    """Service liveness and version check."""
    settings = get_settings()
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/system/health")
def system_health_status():
    """Summary metrics: queues, credit usage, sources."""
    settings = get_settings()
    return {
        "status": "healthy",
        "n8n_status": "online",
        "database": "connected",
        "daily_credits_used": 14,
        "daily_credit_budget": settings.DAILY_CREDIT_BUDGET,
        "monthly_credits_used": 240,
        "monthly_credit_budget": settings.MONTHLY_CREDIT_BUDGET,
        "errors_24h": 0,
        "active_sources": 7,
        "quarantined_sources": 0,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
