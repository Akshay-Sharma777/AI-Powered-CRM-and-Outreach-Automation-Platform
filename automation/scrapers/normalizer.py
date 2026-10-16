"""
Field Normalizer for Scraper Payloads.
Standardizes messy text formats for experience, salary, and location.
Deterministic rule engine. Unparseable input safely returns None.
"""

import re
from typing import Optional, Tuple, Dict, Any


def normalize_experience(raw_text: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    """
    Standardizes experience strings into (min_years, max_years).
    Returns (None, None) if completely unparseable. Never raises an exception.
    """
    if not raw_text or not isinstance(raw_text, str):
        return None, None

    cleaned = raw_text.strip().lower()

    if any(k in cleaned for k in ["fresher", "freshers", "no experience", "0 yrs", "0 years"]):
        return 0, 0

    range_match = re.search(r'(\d+)\s*(?:-|to)\s*(\d+)', cleaned)
    if range_match:
        try:
            return int(range_match.group(1)), int(range_match.group(2))
        except (ValueError, TypeError):
            pass

    single_match = re.search(r'(\d+)', cleaned)
    if single_match:
        try:
            val = int(single_match.group(1))
            return val, val
        except (ValueError, TypeError):
            pass

    return None, None


def normalize_location(raw_text: Optional[str]) -> Optional[str]:
    """Cleans and formats location string."""
    if not raw_text or not isinstance(raw_text, str):
        return None
    cleaned = raw_text.strip()
    if not cleaned:
        return None
    # Capitalize title case
    return cleaned.title()
