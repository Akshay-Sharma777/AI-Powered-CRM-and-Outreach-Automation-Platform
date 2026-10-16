"""
Prompt Injection Guard.
Detects adversarial prompt injection attempts in scraped web data and wraps content in delimiters.
"""

import re
from typing import Tuple, List

SUSPICIOUS_PATTERNS = [
    re.compile(r'ignore\s+(?:all\s+)?previous\s+instructions', re.IGNORECASE),
    re.compile(r'reveal\s+(?:your\s+)?(?:system\s+)?prompt', re.IGNORECASE),
    re.compile(r'system\s+override', re.IGNORECASE),
    re.compile(r'disclose\s+(?:internal\s+)?api\s+keys?', re.IGNORECASE),
    re.compile(r'you\s+are\s+now\s+in\s+developer\s+mode', re.IGNORECASE),
]


def wrap_scraped_data(data_content: str, label: str = "EXTERNAL_SCRAPED_DATA") -> str:
    """Wraps scraped content inside explicit safety boundaries."""
    return f"<{label}>\n{data_content}\n</{label}>"


def inspect_for_injection(text: str) -> Tuple[bool, List[str]]:
    """
    Scans text for prompt injection patterns.
    Returns: (is_safe, list_of_detected_warnings)
    """
    warnings: List[str] = []
    for pattern in SUSPICIOUS_PATTERNS:
        match = pattern.search(text)
        if match:
            warnings.append(f"Potential prompt injection pattern detected: '{match.group(0)}'")

    is_safe = (len(warnings) == 0)
    return is_safe, warnings
