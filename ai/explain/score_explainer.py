"""
Score Explainer Module.
Translates structured confidence scoring reason codes into user-friendly plain English explanations.
Strictly deterministic lookup - no AI call required.
"""

from typing import Dict, List, Any

REASON_TEMPLATES = {
    "OFFICIAL_COMPANY_SOURCE": "Opportunity originated directly from the organization's official careers portal.",
    "VERIFIED_PORTAL_SOURCE": "Discovered via a recognized, quality-checked listing portal.",
    "AGGREGATOR_SOURCE": "Extracted from a third-party job aggregator; manual verification advised.",
    "CONTACT_ROLE_CONFIRMED": "The associated contact is a confirmed talent recruiter or placement official.",
    "CONTACT_ROLE_UNCONFIRMED": "Contact identity found, but explicit recruiter role could not be verified.",
    "EMAIL_VERIFIED_DELIVERABLE": "Email address deliverability confirmed via active SMTP validation.",
    "EMAIL_CATCH_ALL": "Domain configured as a catch-all server; individual inbox deliverability is unconfirmed.",
    "EMAIL_RISKY": "Email mailbox exhibits bounce or deliverability risk flags.",
    "EMAIL_UNVERIFIED": "Email has not undergone deliverability verification.",
    "DATA_VERY_FRESH": "Posting published within the last 72 hours.",
    "DATA_MODERATELY_FRESH": "Posting published within the last 14 days.",
    "DATA_AGED": "Posting published more than two weeks ago.",
    "COMPLETENESS_SCORE": "Record contains essential details including description, location, and requirements.",
    "PUBLICATION_DATE_MISSING": "Original publication date could not be extracted from the source listing.",
    "CONTACT_COMPANY_ASSOCIATION_UNCONFIRMED": "Association between contact and organization requires review."
}


def explain_reason_code(code: str) -> str:
    """Translates a single reason code into an explanatory sentence."""
    return REASON_TEMPLATES.get(code, code)


def explain_scores(reasons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enriches a list of reason code objects with human-readable descriptions."""
    explained = []
    for item in reasons:
        code = item.get("code", "")
        explained.append({
            "code": code,
            "points": item.get("points", 0),
            "explanation": explain_reason_code(code)
        })
    return explained
