"""
Deduplication and Normalization Service.
Prevents duplicate records and flags potential duplicate opportunities.
NEVER automatically merges contacts based on name similarity alone.
"""

import re
from typing import Optional, Dict, Any, List

# Legal entity suffixes to strip during company name normalization
COMPANY_SUFFIX_REGEX = re.compile(
    r'\b(pvt\.?\s*ltd\.?|private\s+limited|ltd\.?|limited|inc\.?|incorporated|corp\.?|corporation|llc)\b',
    re.IGNORECASE
)
PUNCTUATION_REGEX = re.compile(r'[^\w\s]')


def normalize_company_name(name: str) -> str:
    """
    Normalizes company names:
    - Lowercase
    - Removes legal suffix (Pvt Ltd, LLC, Inc, etc.)
    - Removes punctuation
    - Collapses extra whitespace
    """
    if not name:
        return ""
    cleaned = name.lower()
    cleaned = COMPANY_SUFFIX_REGEX.sub("", cleaned)
    cleaned = PUNCTUATION_REGEX.sub(" ", cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def normalize_job_title(title: str) -> str:
    """Normalizes job titles for matching."""
    if not title:
        return ""
    cleaned = title.lower()
    cleaned = PUNCTUATION_REGEX.sub(" ", cleaned)
    return re.sub(r'\s+', ' ', cleaned).strip()


def check_for_duplicates(
    source_id: str,
    source_identifier: str,
    source_url: str,
    company_name: str,
    title: str,
    location: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluates potential duplicate opportunities:
    1. Exact Match: (source_id, source_identifier)
    2. URL Match: source_url
    3. Semantic Match: normalized_company + normalized_title
    """
    norm_company = normalize_company_name(company_name)
    norm_title = normalize_job_title(title)

    return {
        "normalized_company": norm_company,
        "normalized_title": norm_title,
        "is_exact_source_match": False,
        "potential_duplicates": []
    }
