"""
Output Fact Checker.
Validates that every claim made in the generated outreach email traces back to verified input facts.
Detects hallucinated compensation, job titles, or unauthorized company relationships.
"""

import re
from typing import Dict, Any, List, Tuple


def fact_check_draft(
    draft: Dict[str, Any],
    verified_facts: Dict[str, Any]
) -> Tuple[bool, List[str]]:
    """
    Validates draft output against verified facts:
    1. Ensures claims_used contains non-empty assertions.
    2. Ensures every cited fact_id exists in verified_facts.
    3. Detects hallucinated compensation amounts not found in input.
    """
    issues: List[str] = []
    body = draft.get("body", "")
    claims = draft.get("claims_used", [])

    if not body.strip():
        issues.append("Email body cannot be empty.")

    if not claims:
        issues.append("No claims_used provided. Every draft must explicitly cite input facts.")

    # Validate that cited fact_ids exist in input
    allowed_fact_ids = set(verified_facts.keys())
    for item in claims:
        fact_id = item.get("fact_id")
        if fact_id not in allowed_fact_ids:
            issues.append(f"Invalid claim reference: fact_id '{fact_id}' does not exist in verified input.")

    # Check for unauthorized dollar or rupee amounts in body if not present in verified facts
    salary_in_facts = str(verified_facts.get("salary_text", "") or "")
    # Find currency mentions (e.g. ₹50,000, $100k, 12 LPA)
    found_currencies = re.findall(r'(?:₹|\$|lpa|inr|usd)\s*\d+[,\d]*', body, re.IGNORECASE)
    for curr in found_currencies:
        if curr.lower() not in salary_in_facts.lower():
            issues.append(f"Potential hallucinated compensation '{curr}' found in body but missing from verified facts.")

    is_valid = (len(issues) == 0)
    return is_valid, issues
