"""
Experience and Opportunity Type Parser.
Rules and regex patterns first; optional AI fallback for low-confidence messy text.
"""

import re
from typing import Tuple, Optional


def parse_experience(raw_text: Optional[str]) -> Tuple[Optional[int], Optional[int], float]:
    """
    Parses messy experience text strings into (min_years, max_years, confidence).
    Examples:
        - "0-2 yrs" -> (0, 2, 1.0)
        - "Fresher" -> (0, 0, 1.0)
        - "No experience required" -> (0, 0, 0.95)
        - "0 to 1 year" -> (0, 1, 1.0)
        - "1-2 Years" -> (1, 2, 1.0)
        - None or empty -> (None, None, 0.0)
    """
    if not raw_text or not raw_text.strip():
        return (None, None, 0.0)

    text = raw_text.strip().lower()

    # Rule 1: Freshers / No experience keywords
    fresher_keywords = ["fresher", "freshers", "no experience", "0 yrs", "0 years", "entry level", "student", "students"]
    for kw in fresher_keywords:
        if kw in text:
            return (0, 0, 1.0)

    # Rule 2: Range matching (e.g. "0-2 yrs", "0 to 1 year", "1 - 3 yrs")
    range_match = re.search(r'(\d+)\s*(?:-|to)\s*(\d+)\s*(?:yrs|years|yr|year)?', text)
    if range_match:
        min_exp = int(range_match.group(1))
        max_exp = int(range_match.group(2))
        return (min_exp, max_exp, 1.0)

    # Rule 3: Single number matching (e.g. "1 yr", "2+ years", "at least 1 year")
    single_match = re.search(r'(\d+)\+?\s*(?:yrs|years|yr|year)', text)
    if single_match:
        exp = int(single_match.group(1))
        return (exp, exp, 0.85)

    return (None, None, 0.0)
