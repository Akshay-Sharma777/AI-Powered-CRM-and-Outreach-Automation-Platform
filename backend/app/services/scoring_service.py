"""
Data Quality and Confidence Scoring Service.
Rule-driven, explainable 0-100 scoring engine with factor breakdowns and reason codes.
Strictly NO AI in the scoring calculation.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List

SCORING_VERSION = "1.0.0"


def calculate_data_quality_score(
    source_type: str,            # 'official_careers', 'verified_portal', 'aggregator'
    has_contact_role: bool,      # Recruiter or TPO identified
    verification_status: str,    # 'deliverable', 'catch_all', 'risky', 'unknown', 'undeliverable'
    published_days_ago: int,     # 0-3 days, 4-14 days, 15+ days
    has_description: bool,
    has_salary: bool,
    has_location: bool,
    is_suppressed: bool = False
) -> Dict[str, Any]:
    """
    Computes an explainable 0-100 confidence score based on 5 factors:
    1. Source reliability (max 25)
    2. Org and contact association (max 25)
    3. Contact verification evidence (max 20)
    4. Data freshness (max 15)
    5. Completeness and consistency (max 15)
    """
    reasons: List[Dict[str, Any]] = []

    # 1. Source Reliability (Max 25)
    if source_type == "official_careers":
        source_score = 25
        reasons.append({"code": "OFFICIAL_COMPANY_SOURCE", "points": 25, "desc": "Official employer website or portal"})
    elif source_type == "verified_portal":
        source_score = 20
        reasons.append({"code": "VERIFIED_PORTAL_SOURCE", "points": 20, "desc": "Curated source (e.g. Internshala, Unstop)"})
    else:
        source_score = 12
        reasons.append({"code": "AGGREGATOR_SOURCE", "points": 12, "desc": "General jobs aggregator"})

    # 2. Org & Contact Association (Max 25)
    if has_contact_role:
        assoc_score = 25
        reasons.append({"code": "CONTACT_ROLE_CONFIRMED", "points": 25, "desc": "Contact role confirmed relevant"})
    else:
        assoc_score = 10
        reasons.append({"code": "CONTACT_ROLE_UNCONFIRMED", "points": 10, "desc": "Direct recruiter role not verified"})

    # 3. Contact Verification Evidence (Max 20)
    if verification_status == "deliverable":
        verif_score = 20
        reasons.append({"code": "EMAIL_VERIFIED_DELIVERABLE", "points": 20, "desc": "Email verified deliverable"})
    elif verification_status == "catch_all":
        verif_score = 10
        reasons.append({"code": "EMAIL_CATCH_ALL", "points": 10, "desc": "Domain accepts catch-all mail"})
    elif verification_status == "risky":
        verif_score = 5
        reasons.append({"code": "EMAIL_RISKY", "points": 5, "desc": "Email flagged risky by verification provider"})
    else:
        verif_score = 0
        reasons.append({"code": "EMAIL_UNVERIFIED", "points": 0, "desc": "Email unverified or undeliverable"})

    # 4. Data Freshness (Max 15)
    if published_days_ago <= 3:
        fresh_score = 15
        reasons.append({"code": "DATA_VERY_FRESH", "points": 15, "desc": "Published within the last 3 days"})
    elif published_days_ago <= 14:
        fresh_score = 10
        reasons.append({"code": "DATA_MODERATELY_FRESH", "points": 10, "desc": "Published within the last 2 weeks"})
    else:
        fresh_score = 5
        reasons.append({"code": "DATA_AGED", "points": 5, "desc": "Published over 14 days ago"})

    # 5. Completeness & Consistency (Max 15)
    comp_score = 0
    if has_description:
        comp_score += 7
    if has_salary:
        comp_score += 4
    if has_location:
        comp_score += 4

    reasons.append({"code": "COMPLETENESS_SCORE", "points": comp_score, "desc": f"Completeness factors score: {comp_score}/15"})

    total_score = min(100, source_score + assoc_score + verif_score + fresh_score + comp_score)

    # Classify band
    if is_suppressed:
        band = "suppressed"
    elif total_score >= 80:
        band = "high"
    elif total_score >= 60:
        band = "medium"
    else:
        band = "low"

    return {
        "score": total_score,
        "band": band,
        "is_eligible": (band == "high" and not is_suppressed),
        "reasons": reasons,
        "factor_breakdown": {
            "source_reliability": source_score,
            "organization_association": assoc_score,
            "contact_verification": verif_score,
            "data_freshness": fresh_score,
            "completeness": comp_score
        },
        "scoring_version": SCORING_VERSION,
        "scored_at": datetime.now(timezone.utc).isoformat()
    }
